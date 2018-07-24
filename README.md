# GAL: Genome Annotator Light
###### A Docker package for analyzing and visualizing a genome or a group of genomes. 

**Latest Version**: 1.0 
### Source
https://hub.docker.com/u/cglabiicb/

### User Mannual
https://github.com/computational-genomics-lab/GAL/blob/master/User_Guide_Latest.pdf
### Demo Application
- For Blue Green Algee Genomes 
  - www.eumicrobedb.org/bga
- For Fungi Genomes
  - www.eumicrobedb.org/fungi

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
