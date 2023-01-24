# Script to get BPS and Kemendagri desa id
# Date: Jan 24, 2023

from urllib.request import urlopen
import json
import csv
import timeit

start = timeit.default_timer()

# Prepare output location
file = ".../kodedesa_bps_vs_kemendagri.csv"

f = open(file, "w")
headers = "kode_prov_bps, nama_prov_bps, kode_prov_dagri, nama_prov_dagri, \
            kode_kab_bps, nama_kab_bps, kode_kab_dagri, nama_kab_dagri, \
            kode_kec_bps, nama_kec_bps, kode_kec_dagri, nama_kec_dagri, \
            kode_desa_bps, nama_desa_bps, kode_desa_dagri, nama_desa_dagri, \n"
f.write(headers)

# Checking if BPS and Kemendagri have different prov codes
with urlopen ('https://sig.bps.go.id/rest-bridging-dagri/getwilayah?level=provinsi&parent=0') as url:
    results = url.read()
    prov = json.loads(results) # there are 2 uncommon prov codes (Papua Barat and Papua) between BPS and Kemendagri. 
                           
# get prov codes (BPS and Kemendagri)
countprov = len(prov)
for x in range(countprov):
    kode_prov_bps = prov[x]['kode_bps']
    nama_prov_bps = prov[x]['nama_bps']
    kode_prov_dagri = prov[x]['kode_dagri']
    nama_prov_dagri = prov[x]['nama_dagri']
    
    print(prov[x]['nama_bps'])

    # using BPS prov codes, get kabupaten codes (BPS and Kemendagri)
    with urlopen('https://sig.bps.go.id/rest-bridging/getwilayah?level=kabupaten&parent='+prov[x]['kode_bps']) as url:
        results = url.read() 
    kab = json.loads(results)

    countkab = len(kab)
    for i in range(countkab):
        kode_kab_bps = kab[i]['kode_bps']
        nama_kab_bps = kab[i]['nama_bps']
        kode_kab_dagri0 = kab[i]['kode_dagri']
        kode_kab_dagri = kode_kab_dagri0.replace(".", "")
        nama_kab_dagri = kab[i]['nama_dagri']
        
        print(kab[i]['nama_bps'])

        # using BPS kabupaten codes, get kecamatan codes (BPS and Kemendagri) 
        with urlopen('https://sig.bps.go.id/rest-bridging/getwilayah?level=kecamatan&parent='+kab[i]['kode_bps']) as url:
            results = url.read()
        kec = json.loads(results)

        countkec = len(kec)
        for j in range(countkec):
            kode_kec_bps = kec[j]['kode_bps']
            nama_kec_bps = kec[j]['nama_bps']
            kode_kec_dagri0 = kec[j]['kode_dagri']
            kode_kec_dagri = kode_kec_dagri0.replace(".", "")
            nama_kec_dagri = kec[j]['nama_dagri']

            # using BPS kecamatan codes, get kelurahan/desa codes (BPS and Kemendagri)
            with urlopen('https://sig.bps.go.id/rest-bridging/getwilayah?level=desa&parent='+kec[j]['kode_bps']) as url:
                results = url.read()
            desa = json.loads(results)

            countdesa = len(desa)
            for k in range(countdesa):
                kode_desa_bps = desa[k]['kode_bps']
                nama_desa_bps = desa[k]['nama_bps']
                kode_desa_dagri0 = desa[k]['kode_dagri']
                kode_desa_dagri = kode_desa_dagri0.replace(".", "")
                nama_desa_dagri = desa[k]['nama_dagri']
                
                f.write('"{}"'.format(kode_prov_bps) +
                    ',"{}"'.format(nama_prov_bps) +
                    ',"{}"'.format(kode_prov_dagri) +
                    ',"{}"'.format(nama_prov_dagri) +
                    ',"{}"'.format(kode_kab_bps) +
                    ',"{}"'.format(nama_kab_bps) +
                    ',"{}"'.format(kode_kab_dagri) +
                    ',"{}"'.format(nama_kab_dagri) +
                    ',"{}"'.format(kode_kec_bps) +
                    ',"{}"'.format(nama_kec_bps) +
                    ',"{}"'.format(kode_kec_dagri) +
                    ',"{}"'.format(nama_kec_dagri) +
                    ',"{}"'.format(kode_desa_bps) + 
                    ',"{}"'.format(nama_desa_bps) + 
                    ',"{}"'.format(kode_desa_dagri) +
                    ',"{}"'.format(nama_desa_dagri) + "\n")
                
        # f.flush()
            
f.close()

end = timeit.default_timer()
print(end - start) # running time ~ 4100 seconds




