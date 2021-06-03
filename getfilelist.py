from despydb import  desdbi
import numpy as np
import astropy.io.fits as pyfits
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

PROPIDS="'2019A-0065', '2019B-0910', '2021A-0037', '2019B-0304', '2019B-0219', '2021A-0113'"
def get_exps(PROPIDS):
  dbh = desdbi.DesDbi(section='db-desoper-deca')
  cur = dbh.cursor()
  query= """ 
  with 
     images as (
        select 
           i.expnum as expnum, i.ccdnum as ccdnum, i.band as band, racmin, racmax, deccmin, deccmax, fai.path||'/'||i.filename||fai.compression as ilink 
        from 
           decade.proctag t, decade.image i, decade.file_archive_info fai, decade.exposure x 
        where 
           t.tag='DECADE_FINALCUT' and t.pfw_attempt_id=i.pfw_attempt_id and i.filetype='red_immask' and i.filename=fai.filename and i.expnum = x.expnum and PROPID in ({0}) 
        order by 
           expnum, ccdnum
     ),  
     catalogs as (
        select 
           c.expnum as expnum, c.ccdnum as ccdnum, fai.path||'/'||c.filename||fai.compression as clink 
        from 
           decade.proctag t, decade.catalog c, decade.file_archive_info fai, decade.exposure x  
        where 
           t.tag='DECADE_FINALCUT' and t.pfw_attempt_id=c.pfw_attempt_id and c.filetype='cat_finalcut' and c.filename=fai.filename and c.expnum = x.expnum and PROPID in ({1}) 
        order by 
           expnum, ccdnum
     ), 
     psfs as (
        select 
           m.expnum as expnum, m.ccdnum as ccdnum, fai.path||'/'||m.filename||fai.compression as plink 
        from 
           decade.proctag t, decade.miscfile m, decade.file_archive_info fai, decade.exposure x  
        where 
           t.tag='DECADE_FINALCUT' and t.pfw_attempt_id=m.pfw_attempt_id and m.filetype='psfex_model' and m.filename=fai.filename and m.expnum = x.expnum and PROPID in ({2}) 
        order by 
           expnum, ccdnum
     ) 
  select 
     images.expnum as expnum, images.ccdnum as ccdnum, band, racmin, racmax, deccmin, deccmax, ilink, clink, plink
  from 
     images, catalogs, psfs 
  where 
     images.expnum = catalogs.expnum 
     and images.ccdnum = catalogs.ccdnum 
     and images.expnum = psfs.expnum 
     and images.ccdnum = psfs.ccdnum
""".format(PROPIDS,PROPIDS,PROPIDS)

  cur.execute(query)
  rows=np.array(cur.fetchall())

  np.savetxt("file_list.txt", rows, fmt="%s")  

def count_exps(PROPIDS):
  dbh = desdbi.DesDbi(section='db-desoper-deca')
  cur = dbh.cursor()
  query= """
  select
     PROPID, count(expnum) as N_EXP
  from
     decade.exposure
  where 
     PROPID in ({0})
  group by
     PROPID
  order by
     PROPID
""".format(PROPIDS) 

  cur.execute(query)
  rows=np.array(cur.fetchall())
  for row in rows:
    print (row)



find_raws(PROPIDS)
count_exps(PROPIDS)

