# Data 
## GWAS Catalog
* GWAS Catalog is a collection of all published GWAS assaying at least 100,000 SNPs and all SNP-trait associations with p-values $< 1.0*10^{-5}$. Data in the GWAS Catalog is extracted from the literature. Extracted information includes *publication information*, *study cohort information* such as cohort size, country of recruitment and subject ethnicity, and *SNP-diease association information* including SNP identifier (i.e. RSID), p-value, gene and risk allele. 

* This project mainly focuses on the data from [GWAS Catalog](https://www.ebi.ac.uk/gwas/). To be specific, data are download from [GWAS Diagram](https://www.ebi.ac.uk/gwas/diagram). For this part, we only consider the binary categorical traits. 

## 1000 Genomes
* The 1000 Genomes Project was an international research effort to establish by far the most detailed catalogue of human genetic variation (from [wikipedia](https://en.wikipedia.org/wiki/1000_Genomes_Project)). The goal of the 1000 Genomes Project is to provide a resource of almost all variants, including SNPs and structural variants, and their haplotype contexts. This resource will allow genome-wide association studies to focus on almost all variants that exist in regions found to be associated with disease (from [NIH](https://www.genome.gov/27528684/1000-genomes-project/)). 

* In 1000 Genomes includes people from [26](http://www.internationalgenome.org/faq/which-populations-are-part-your-study) different populations. In this project, we only focus on "CEU" (Utah Residents (CEPH) with Northern and Western European Ancestry). Data can be download from this [Link](ftp://ftp.1000genomes.ebi.ac.uk/vol1/ftp/release/20130502/). 

## OpenSNP
* openSNP is an open source website where users can upload their genetic test results and share their phenotypes. Users can access through this [Link](https://opensnp.org/).

# Publications
In this part, we published one conference paper and one journal paper. All the codes of experiments in the papers are included in this repository. 

[1] Lu Zhang, Qiuping Pan, Xintao Wu, and Xinhua Shi. Building Bayesian Networks from GWAS statistics based on Independence of Causal Influence. In Bioinformatics and Biomedicine (BIBM), 2016 IEEE International Conference on (2016), IEEE.

[2] Lu Zhang, Qiuping Pan, Xintao Wu, and Xinhua Shi. Bayesian Network Construction and Genotype-phenotype Inference using GWAS Statistics. IEEE/ACM Transactions on Computational Biology and Bioinformatics 99 (2017).