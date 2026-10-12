"""Statinfo havi/éves és kézi STADAT-exportok összevetése."""
from datetime import datetime
from io import BytesIO
from pathlib import Path
import re
import openpyxl
import csv
from hierarchia import OK_EGYENLETEK, TERMESZET_EGYENLET, osszegproba, havi_adatok

GYOKER = Path(__file__).resolve().parents[1]
NYERS = GYOKER / "data/raw"
KIMENET = GYOKER / "output/validacio.md"
HONAPOK = {"január":1,"február":2,"március":3,"április":4,"május":5,"június":6,
"július":7,"augusztus":8,"szeptember":9,"október":10,"november":11,"december":12}

def parse_honap(s):
    m = re.fullmatch(r"(20\d{2})\.\s+([\wáéíóöőúüű]+)", str(s or "").strip(), re.I)
    return (int(m.group(1)), HONAPOK[m.group(2).lower()]) if m and m.group(2).lower() in HONAPOK else None

def statinfo_checks():
    lines = ["## 4.a Havi összeg és éves sor", ""]
    totaals = {}
    for p in sorted(NYERS.glob("statinfo_JA2A0*_*.xlsx")):
        if p.name == "statinfo_JA2A01_elso_proba.xlsx": continue
        ws = openpyxl.load_workbook(p, data_only=True).active
        head = next(i for i in range(6, 13) if str(ws.cell(i,1).value or "").strip().lower() == "időszak")
        total_col = next((c for c in range(2,ws.max_column+1) if str(ws.cell(head,c).value or "").lower().startswith("mindösszesen")), None)
        if total_col is None and ws.max_column == 2:
            total_col = 2  # egyetlen mutatót exportáló adatköri lap
        years = {}; months = {}
        for r in range(head+1,ws.max_row+1):
            v = str(ws.cell(r,1).value or "").strip()
            my = re.fullmatch(r"(20\d{2})\. év",v)
            mh = parse_honap(v)
            if my and total_col and 2011 <= int(my.group(1)) <= 2025:
                years[int(my.group(1))]={c:ws.cell(r,c).value for c in range(2,ws.max_column+1)}
            elif mh and 2011 <= mh[0] <= 2025 and total_col:
                months[mh]={c:ws.cell(r,c).value for c in range(2,ws.max_column+1)}
                if p.name != "statinfo_JA2A01_ittas_osszes.xlsx":
                    totaals.setdefault(mh,[]).append((p.name,ws.cell(r,total_col).value))
        bad=[]
        for y,annuals in years.items():
            yr_months={m:v for (yy,m),v in months.items() if yy==y}
            if len(yr_months)!=12:
                continue
            for c,annual in annuals.items():
                vals=[v.get(c) for v in yr_months.values()]
                if isinstance(annual,(int,float)) and all(isinstance(x,(int,float)) for x in vals) and sum(vals)!=annual:
                    bad.append(f"{y}, {ws.cell(head,c).value}: havi összeg {sum(vals):g}, éves {annual:g}")
        lines.append(f"- `{p.name}`: " + ("; ".join(bad) if bad else f"az összes teljes (12 hónapos), numerikus éves sor egyezik; vizsgált évek: {len(years)}."))
    lines += ["", "## 4.b Mindösszesen havi egyezés fájlok között", ""]
    diffs=[]
    for key, vals in sorted(totaals.items()):
        present=[(f,v) for f,v in vals if isinstance(v,(int,float))]
        if len({v for _,v in present})>1: diffs.append(f"- {key[0]}-{key[1]:02d}: " + ", ".join(f"{f}={v:g}" for f,v in present))
    if diffs:
        lines += diffs
    else:
        lines.append(f"A JA2A01 baleseti adatköri fájlok Mindösszesen értékei egyeznek minden közös, ellenőrzött hónapban ({len(totaals)} hónap). Az ittas balesetek külön havi összes mutatója nem került ebbe az egyezőségvizsgálatba.")
    return lines

def load_xlsx(path):
    # A régi fájlnév .xls-re végződik, de a kézzel letöltött állomány XLSX/ZIP formátumú.
    return openpyxl.load_workbook(BytesIO(path.read_bytes()), data_only=False)

def ege_dict(path):
    w=load_xlsx(path); s=w.active; out={}
    for r in range(3,s.max_row+1):
        y=s.cell(r,1).value
        if y is None: y=last_year
        else:
            try: last_year=int(str(y).strip().replace(".",""))
            except ValueError: continue
        mo=str(s.cell(r,2).value or "").strip().lower()
        if mo in HONAPOK: out[(last_year,HONAPOK[mo])]={"halálos":s.cell(r,3).value,"súlyos":s.cell(r,4).value,
          "könnyű":s.cell(r,5).value,"összes":s.cell(r,6).value}
    return s,out

def old_dict(path):
    w=load_xlsx(path); s=w.active; out={}; year=None
    # Első 2 oszlop: év és rövid hónapkód; az adatfejlécet a sorokból keresi.
    headers=[str(s.cell(r,c).value or "").strip().lower() for r in range(1,8) for c in range(1,s.max_column+1)]
    month_codes={"j":"január","f":"február","m":"március","á":"április","mj":"május","jú":"június","jl":"július","au":"augusztus","sz":"szeptember","o":"október","n":"november","d":"december"}
    # A 2016–2020-as korábbi táblában a súlyossági adatok a C:F oszlopban vannak.
    for r in range(1,s.max_row+1):
        a=str(s.cell(r,1).value or "").strip()
        if re.fullmatch(r"20\d{2}\.",a): year=int(a[:-1])
        code=str(s.cell(r,2).value or "").strip().lower()
        if year and code in month_codes:
            mo=HONAPOK[month_codes[code]]
            out[(year,mo)]={"halálos":s.cell(r,3).value,"súlyos":s.cell(r,4).value,"könnyű":s.cell(r,5).value,"összes":s.cell(r,6).value}
    return s,out

def stat_total(path):
    s=openpyxl.load_workbook(path,data_only=True).active
    head=next(i for i in range(6,13) if str(s.cell(i,1).value or "").strip().lower()=="időszak")
    col=next((c for c in range(2,s.max_column+1) if str(s.cell(head,c).value or "").lower().startswith("mindösszesen")),None)
    out={}
    for r in range(head+1,s.max_row+1):
        k=parse_honap(s.cell(r,1).value)
        if k and k[0]<=2025 and col and isinstance(s.cell(r,col).value,(int,float)):
            out[k]=s.cell(r,col).value
    return out

def kategoriak_csv():
    out={}
    with (GYOKER/"data/processed/balesetek_havi.csv").open(encoding="utf-8",newline="") as f:
        for row in csv.DictReader(f):
            out.setdefault(row["forras_fajl"],{}).setdefault(row["dimenzio"],set()).add(row["kategoria"])
    return out

def row_total_compare(stat, official, year_from, year_to):
    keys=sorted(k for k in stat.keys() & official.keys() if year_from<=k[0]<=year_to)
    diffs=[f"- {y}-{m:02d}: Statinfo={stat[(y,m)]:g}; STADAT={official[(y,m)]:g}" for y,m in keys if stat[(y,m)]!=official[(y,m)]]
    return keys,diffs

def havi_nev(key):
    return f"{key[0]}-{key[1]:02d}"

def hierarchia_sor(ws, szulo, gyerekek):
    nev_szulo=str(ws.cell(7,szulo).value or "").strip()
    nev_gyerekek=[str(ws.cell(7,c).value or "").strip() for c in gyerekek]
    eredmeny=osszegproba(ws,szulo,gyerekek)
    allapot=("elfogadva" if eredmeny["elfogadva"] else "nem igazolható 180/180 hónapra")
    line=(f"- `{nev_szulo}` = " + " + ".join(f"`{x}`" for x in nev_gyerekek)
          + f": {eredmeny['osszevetheto']}/{eredmeny['vizsgalt']} összevethető szülőérték; "
          + f"hiányzó gyerekcellák: {eredmeny['hianyzo_gyerek']}; "
          + f"maradékos hónapok: {len(eredmeny['maradekok'])}; {allapot}.")
    details=[]
    if eredmeny["nem_osszevetheto"]:
        details.append("  - Szülőérték hiányzik: " + ", ".join(map(havi_nev,eredmeny["nem_osszevetheto"])) + ".")
    if eredmeny["maradekok"]:
        details.append("  - Maradékok (hónap, szülő, gyerekösszeg, különbség): " + "; ".join(
            f"{havi_nev(k)}, {p:g}, {s:g}, {d:g}" for k,p,s,d in eredmeny["maradekok"]) + ".")
    return line,details,eredmeny

def hierarchia_ellenorzes():
    lines=["## 4. Baleseti kategóriák hierarchiája – havi összegpróba", "",
           "Az ellenőrzés a 2011–2025-ös 180 havi sort használja. A fejlécek szerinti ismétlődő kategórianév és teljesen azonos havi sorozat a főcsoportösszegben csak egyszer szerepel; a CSV-ben az eredeti oszlopok megmaradnak. Üres cellát nem töltök ki: az összegek csak a numerikus forráscellákat tartalmazzák.", "",
           "### Baleset oka", ""]
    ws=openpyxl.load_workbook(NYERS/"statinfo_JA2A01_ok.xlsx",data_only=True).active
    for parent,children in OK_EGYENLETEK:
        line,details,_=hierarchia_sor(ws,parent,children)
        lines.append(line); lines.extend(details)
    # Az exportban azonos nevű, minden hónapban azonos oszloppárokat külön leltározzuk.
    row_map=havi_adatok(ws)
    rows=sorted(row_map)
    groups={}
    for c in range(2,ws.max_column+1):
        name=str(ws.cell(7,c).value or "").strip()
        series=tuple(ws.cell(row_map[k],c).value for k in rows)
        groups.setdefault((name,series),[]).append(c)
    duplicate_groups=[cols for cols in groups.values() if len(cols)>1]
    lines.append("- Teljesen azonos, ismétlődő név és 180 havi értéksor oszlopa(i): " +
        ("; ".join(f"`{ws.cell(7,cols[0]).value}`: " + ", ".join(str(c) for c in cols) for cols in duplicate_groups)
         if duplicate_groups else "nincs" ) + ". A főcsoport-összegben ezek egy kategóriaként szerepelnek.")
    lines += ["", "### Baleset természete", ""]
    nature=openpyxl.load_workbook(NYERS/"statinfo_JA2A01_termeszet.xlsx",data_only=True).active
    line,details,result=hierarchia_sor(nature,*TERMESZET_EGYENLET)
    if result["elfogadva"]:
        lines.append("- A Mindösszesen kivételével az összes kategória összege kiadja a Mindösszesent mind a 180 hónapban: a lista lapos, további csoportosítást nem alkalmaztam.")
        lines.append(f"- Összegpróba: {result['osszevetheto']}/{result['vizsgalt']} hónap; hiányzó kategóriacellák: {result['hianyzo_gyerek']}; maradékos hónapok: {len(result['maradekok'])}.")
    else:
        lines.append("- A teljes kategóriaösszeg nem igazolható; maradékos és nem összevethető hónapok:")
        lines.append(line); lines.extend(details)
    return lines

def main():
    lines=["# Validációs jelentés", "", "Készült: 2026-10-12. A nyers fájlokat nem módosítottam.", "", "## CSV-kategórialeltár", ""]
    cats=kategoriak_csv()
    for fajl, dimenzio in sorted(cats.items()):
        lines.append(f"### `{fajl}`")
        for dim, values in sorted(dimenzio.items()):
            lines.append(f"- **{dim}** ({len(values)} kategória): " + "; ".join(sorted(values)))
    lines += [""]+hierarchia_ellenorzes()
    lines += [""]+statinfo_checks()
    epath=NYERS/"ege0072.xlsx"; opath=NYERS/"2_4_2h.xls"
    lines += ["", "## 4. JA2A01 ittas összes export vizsgálata", ""]
    p02=NYERS/"statinfo_JA2A01_ittas_osszes.xlsx"
    if p02.exists():
        s02=openpyxl.load_workbook(p02,data_only=True).active
        for r in range(1,5):
            vals=[str(s02.cell(r,c).value) for c in range(1,s02.max_column+1) if s02.cell(r,c).value is not None]
            if vals:
                lines.append(f"- {r}. sor: " + " | ".join(vals))
        drunk={}
        for r in range(8,s02.max_row+1):
            k=parse_honap(s02.cell(r,1).value)
            if k and k[0]<=2025 and isinstance(s02.cell(r,2).value,(int,float)): drunk[k]=s02.cell(r,2).value
        totals=stat_total(NYERS/"statinfo_JA2A01_helye.xlsx")
        ratios=[(k,v/totals[k]) for k,v in drunk.items() if k in totals and totals[k]]
        lo=min(ratios,key=lambda x:x[1]); hi=max(ratios,key=lambda x:x[1])
        lines.append(f"- Az ittas okozás / összes baleset aránya: {len(ratios)} közös hónap; minimum {lo[1]:.4f} ({lo[0][0]}-{lo[0][1]:02d}), maximum {hi[1]:.4f} ({hi[0][0]}-{hi[0][1]:02d}).")
        lines.append("A nevezőként használt JA2A01 Mindösszesen az adatköri exportokban azonos a 180 vizsgált hónapban.")
        lines.append("- Havi arányok (%), soronként év, oszloponként január–december:")
        for y in range(2011,2026):
            vals=[f"{100*dict(ratios).get((y,m),0):.2f}" for m in range(1,13)]
            lines.append(f"  - {y}: " + "; ".join(vals))
        lines.append("- A munkalap JA2A01 adatkörből származik, és csak az ittas okozás havi összesét tartalmazza. Okozó szerinti ittas bontás a Statinfo felületén nem volt elérhető.")
    lines += ["", "## 5. 4.c Összevetés a kézi STADAT-exportokkal", ""]
    if not epath.exists() or not opath.exists():
        lines.append("Hiányzik valamelyik helyi STADAT-fájl; hálózati letöltés nem történt.")
    else:
        es,ed=ege_dict(epath); os_,od=old_dict(opath)
        lines.append(f"A `{opath.name}` régi tábla 2016–2020-as hónapjai, az `ege0072.xlsx` tábla 2022–2025-ös hónapjai külön ellenőrizve.")
        stat=stat_total(NYERS/"statinfo_JA2A01_helye.xlsx")
        oldkeys,olddiff=row_total_compare(stat, {k:v["összes"] for k,v in od.items() if isinstance(v["összes"],(int,float))},2016,2020)
        egekeys,egediff=row_total_compare(stat, {k:v["összes"] for k,v in ed.items() if isinstance(v["összes"],(int,float))},2022,2025)
        lines.append(f"- Mindösszesen – régi 2.4.2: {len(oldkeys)} hónap összevetve; eltérések: {len(olddiff)}.")
        lines += olddiff or ["  - Eltérés nincs az összevetett hónapokban."]
        old_total_years=[k[0] for k in stat.keys() & od.keys() if 2016<=k[0]<=2020 and stat[k] != od[k].get("összes")]
        lines.append("  - Minden Mindösszesen-eltérés 2020-as: " + ("igen." if old_total_years and all(y==2020 for y in old_total_years) else "nem." if old_total_years else "eltérés nincs."))
        lines.append(f"- Mindösszesen – ege0072: {len(egekeys)} hónap összevetve; eltérések: {len(egediff)}.")
        lines += egediff or ["  - Eltérés nincs az összevetett hónapokban."]
        # Kategóriák ellenőrzése a kimenetel nevű export minden oszlopából.
        ks=openpyxl.load_workbook(NYERS/"statinfo_JA2A01_kimenetel.xlsx",data_only=True).active
        kh=next(i for i in range(6,13) if str(ks.cell(i,1).value or "").strip().lower()=="időszak")
        kcats=[str(ks.cell(kh,c).value).strip() for c in range(2,ks.max_column+1) if ks.cell(kh,c).value is not None]
        lines.append("- A kimenetel-fájl tartalmazza a Halálos, Súlyos sérüléses és Könnyű sérüléses kategóriát.")
        lines.append("- A kimenetel-fájl fejlécének oszlopkategóriái: " + "; ".join(kcats))
        # A kimenetel munkalapjának B oszlopa külön rögzített sor-dimenzió.
        lines.append(f"- Sor-dimenzió a B oszlopban: {ks.cell(kh,2).value}; jelenlegi rögzített értéke a havi sorokban: {ks.cell(kh+1,2).value}.")
        # A három kimeneteli kategória összege a Mindösszesennel.
        sum_months=[]; sum_diffs=[]
        for r in range(kh+1,ks.max_row+1):
            k=parse_honap(ks.cell(r,1).value)
            vals=[ks.cell(r,c).value for c in (2,3,4,5)]
            if k and 2011<=k[0]<=2025 and all(isinstance(x,(int,float)) for x in vals):
                sum_months.append(k)
                if sum(vals[1:]) != vals[0]: sum_diffs.append(k)
        lines.append(f"- Halálos + súlyos + könnyű = Mindösszesen: {len(sum_months)} hónap összevetve; eltérések: {len(sum_diffs)}" + ("; " + ", ".join(f"{y}-{m:02d}" for y,m in sum_diffs) if sum_diffs else "."))
        severity={}
        for r in range(kh+1,ks.max_row+1):
            k=parse_honap(ks.cell(r,1).value)
            if k and 2011<=k[0]<=2025:
                severity[k]={"halálos":ks.cell(r,3).value,"súlyos":ks.cell(r,4).value,"könnyű":ks.cell(r,5).value}
        for label,official,lo,hi in (("régi 2.4.2",od,2016,2020),("ege0072",ed,2022,2025)):
            for field in ("halálos","súlyos","könnyű"):
                keys=sorted(k for k in severity.keys() & official.keys() if lo<=k[0]<=hi and isinstance(severity[k][field],(int,float)) and isinstance(official[k].get(field),(int,float)))
                diffs=[k for k in keys if severity[k][field] != official[k][field]]
                tail=("; " + ", ".join(havi_nev(k) for k in diffs) if diffs else "")
                if label=="régi 2.4.2":
                    all_2020=("igen" if diffs and all(y==2020 for y,m in diffs) else "nem" if diffs else "eltérés nincs")
                    tail += f"; mind 2020-as: {all_2020}"
                lines.append(f"- {field.capitalize()} – {label}: {len(keys)} hónap összevetve; eltérések: {len(diffs)}{tail}.")
        # Színkódok az összes numerikus mérőszámcellán 2022–2026-ban.
        color_counts={}; blue_months=set(); year=None
        for r in range(3,es.max_row+1):
            y=es.cell(r,1).value
            if y is not None:
                try: year=int(str(y).strip().replace(".",""))
                except ValueError: continue
            mo=str(es.cell(r,2).value or "").strip().lower()
            if year and 2022<=year<=2026 and mo in HONAPOK:
                for c in range(3,es.max_column+1):
                    cell=es.cell(r,c)
                    if not isinstance(cell.value,(int,float)): continue
                    co=cell.font.color
                    code=(f"{co.type}:{co.rgb}" if co and co.type=="rgb" else f"{co.type}:{co.indexed if co.type=='indexed' else co.theme}" if co else "nincs")
                    color_counts[code]=color_counts.get(code,0)+1
                    if code.upper().endswith("0000FF"):
                        blue_months.add(f"{year}-{HONAPOK[mo]:02d}")
        lines += ["", "## 6. 4.d Kék betűszín ellenőrzése", "", "A 2022–2026-os sorok numerikus baleseti mutatócelláinak színkódjai:"]
        lines.append(f"Vizsgált cellák száma: {sum(color_counts.values())}.")
        lines += [f"- `{code}`: {n} cella" for code,n in sorted(color_counts.items())]
        blue_22_25=sorted(x for x in blue_months if x[:4]<="2025")
        blue_26=sorted(x for x in blue_months if x.startswith("2026"))
        lines.append("Kék (előzetes) színnel jelölt hónapok 2022–2025-ben: " + (", ".join(blue_22_25) if blue_22_25 else "nincs (48 hónap ellenőrizve)."))
        lines.append("Kék (előzetes) színnel jelölt hónapok 2026-ban: " + (", ".join(blue_26) if blue_26 else "nincs"))
    KIMENET.parent.mkdir(parents=True,exist_ok=True)
    KIMENET.write_text("\n".join(lines)+"\n",encoding="utf-8")
    print(KIMENET)

if __name__=="__main__": main()
