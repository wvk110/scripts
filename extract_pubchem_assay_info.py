import os,sys
import numpy
import gzip
import glob
import zipfile


f_w = open("pubchem_assay_info.txt","w")
f_w.write("AID" + "\t" + "GENEID" + "\t" + "TAXONOMY" + "\t" + "ORGANISM" + "\t" +  "INSTITUTION" +"\t"+ "ASSAY_NAME" + "\t" + "ASSAY_DESCRIPTION" + "\t" + "ASSAY_COMMENT" + "\t" + "ASSAY_CATEGORY" + "\t" +"URL" + "\n")
AID_tag_F = "<PC-ID_id>"
AID_tag_R = "</PC-ID_id>"
geneid_tag_F = "<PC-XRefData_gene>"
geneid_tag_R = "</PC-XRefData_gene>"
taxonomy_tag_F = "<Object-id_id>"
taxonomy_tag_R = "</Object-id_id>"
organism_tag_F = "<BinomialOrgname_genus>"
organism_tag_R = "</BinomialOrgname_genus>"
assay_name_tag_F = "<PC-AssayDescription_name>"
assay_name_tag_R = "</PC-AssayDescription_name>"
assay_description_tag_F = "<PC-AssayDescription_description_E>"
assay_description_tag_R = "</PC-AssayDescription_description_E>"
assay_description_comment_tag_F = "<PC-AssayDescription_comment_E>"
assay_description_comment_tag_R = "</PC-AssayDescription_comment_E>"
patent_info_F = "<PC-XRefData_patent>"
patent_info_R = "</PC-XRefData_patent>"
category_F = 'PC-AssayDescription_activity-outcome-method value="'
category_R = '">'
institution_tag_F = "<PC-DBTracking_name>"
institution_tag_R = "</PC-DBTracking_name>"

zip_dirs = glob.glob('./*.zip')  #今いるフォルダにあるzipファイル一覧をリストとして取得
for dir in zip_dirs:  #リストにあるzipファイルを順番に処理
    print(dir[:-4])
    with zipfile.ZipFile(dir, "r") as zf:
        #print(zf)
        name = os.path.dirname(dir)
        zf.extractall(name)
        os.chdir(dir[:-4])
        for filename in (d for d in os.listdir("./")):
            #print(filename)
            aid ="-"
            geneid = "-"
            taxonomy = "-"
            organism ="-"
            assay_name ="-"
            assay_description="-"
            assay_comment ="-"
            category ="-"
            institution = ""
            URL ="https://pubchem.ncbi.nlm.nih.gov/bioassay/"
            with gzip.open(filename, "rt") as fi:
                for line in fi:
                    #print(line[:-1])
                    if AID_tag_F in line and AID_tag_F in line:
                        F_posi = line.find(AID_tag_F)
                        aid = line[F_posi+len(AID_tag_F):-(len(AID_tag_R)+1)]
                        URL = URL + aid
                    elif geneid_tag_F in line and geneid_tag_R in line:
                        F_posi = line.find(geneid_tag_F)
                        geneid= line[F_posi+len(geneid_tag_F):-(len(geneid_tag_R)+1)]
                    elif taxonomy_tag_F in line and taxonomy_tag_R in line:
                        F_posi = line.find(taxonomy_tag_F)
                        taxonomy = line[F_posi+len(taxonomy_tag_F):-(len(taxonomy_tag_R)+1)]
                    elif organism_tag_F in line and organism_tag_R in line:
                        F_posi = line.find(organism_tag_F)
                        organism = line[F_posi+len(organism_tag_F):-(len(organism_tag_F)+1)]                                           
                    elif assay_name_tag_F in line and assay_name_tag_R in line:
                        F_posi = line.find(assay_name_tag_F)
                        assay_name = line[F_posi+len(assay_name_tag_F):-(len(assay_name_tag_R)+1)]
                    elif assay_description_tag_F  in line and assay_description_tag_R in line:
                        F_posi = line.find(assay_description_tag_F)
                        assay_description= line[F_posi+len(assay_description_tag_F ):-(len(assay_description_tag_R)+1)]
                    elif assay_description_comment_tag_F in line and assay_description_comment_tag_R in line:
                        F_posi = line.find(assay_description_comment_tag_F)
                        assay_comment = line[F_posi+len(assay_description_comment_tag_F):-(len(assay_description_comment_tag_R)+1)]
                    elif category_F in line and category_R in line:
                        F_posi = line.find(category_F)
                        R_posi = line.find(category_R)
                        category = line[F_posi+len(category_F):-(len(line))+R_posi]
                        #print(category)
                    elif institution_tag_F in line and institution_tag_R in line:
                        F_posi = line.find(institution_tag_F)
                        institution = line[F_posi+len(institution_tag_F):-(len(institution_tag_R)+1)]
                #print(aid + "\t" + geneid + "\t" + taxonomy + "\t" + organism + "\t" + assay_name + "\t" + assay_description + "\t" + assay_comment + "\t" + category)
                f_w.write(aid + "\t" + geneid + "\t" + taxonomy + "\t" + organism + "\t" +  institution +"\t"+ assay_name + "\t" + assay_description + "\t" + assay_comment + "\t" + category + "\t" + URL + "\n")

    os.chdir("../")
    shutil.rmtree(dir[:-4])