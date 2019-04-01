# GAL: Genome Annotator Light
###### A Docker package for analyzing and visualizing a genome or a group of genomes. 

**Latest Version**: 1.1
### Source
https://hub.docker.com/u/cglabiicb/

### User Mannual
https://github.com/computational-genomics-lab/GAL/blob/master/User_Guide_Latest.pdf
### Demo Application
- For Blue Green Algee Genomes 
  - www.eumicrobedb.org/cglab
### Publication
GAL paper is recently published in ***Genomics***.  

**Please cite:**  
Panda A, Chaudhari NM, Tripathy S. Genome Annotator Light (GAL): A Docker-based package for genome analysis and visualization. *Genomics*. 2019 Mar 26.  
DOI: https://doi.org/10.1016/j.ygeno.2019.03.012  

## Quick Start
 - Once Docker is set up on the host computer, GAL can be downloaded and installed using the following command:
    ```
    docker pull cglabiicb/gal
    ``` 
    This will fetch the latest version with 'latest' tag.
 - To run GAL use the following command:
   ```
   docker run -it -p 8080:80 cglabiicb/gal
   ```

    This will initiate GAL at port 8080 of local server or localhost. The user may use another port to initiate another instance.
    
    [To manipulate Docker utilities refer to Docker Documentation]
 - While the GAL instance is running inside Docker container, GAL User Interface (UI) can be accessed through a web browser at following URL:
   - http://localhost:8080/ or
   - http://IP_ADDRESS_OF_HOST_COMPUTER:8080
        
 - GAL can now be used to upload your data using the browser.

### Bug report
Please use this github portal to report any bug.


### Performance

| __Annotation Type__ | __Organism Name__ | __Genome Size (MB)__ | __System Requirement__ | __Processing Time__ |
|---------------------|-------------------|-----------------|--------------------------|---------------------|
| Genbank| *Candidatus Protochlamydia amoebophila* UWE25|  2.41          | RAM 16GB; 4 core, 3.3 GHz           |  8m  |
| Genbank| *Colletotrichum fioriniae* PJ7 |  49.00          | RAM 16GB; 4 core, 3.3 GHz            |  1h5m  |
| Genbank| *Melampsora larici-populina* 98AG31|  101.13          | RAM 16GB; 4 core, 3.3 GHz           |  1h15m  |
| Genbank| *Drosophila grimshawi* |  200.47          | RAM 16GB; 4 core, 3.3 GHz           | 1h22m  |
| **In-build Demo Data** |
| Genbank| *Lactobacillus casei* str. Zhang|  2.8          | RAM 16GB; 40 core, 2.20GHz           |  15m  |
| Product| *Abiotrophia defectiva* ATCC 49176|  2.04          | RAM 16GB; 40 core, 2.20GHz           |  7m  |
| Minimal| *Rhodotorula graminis* WP1|  21          | RAM 16GB; 40 core, 2.20GHz           |  42m  |
| No Annotation| *Escherichia coli* PA5|  5.3          | RAM 16GB; 40 core, 2.20GHz           |  47m  |

