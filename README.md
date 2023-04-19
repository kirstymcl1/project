# EGM722: Project Assignment

# Introduction
This project focuses on analysing crimes reported within Northern Ireland during February 2023, at both ward level and county level. 

# Set Up 
Before running the code, git and conda will need to be downloaded onto you computer. The instructions for installing git can be found here: https://git-scm.com/downloads and for Anaconda here: https://docs.anaconda.com/free/anaconda/getting-started/install/ 

Now that git and conda have been installed, the repository (https://github.com/kirstymcl1/project) needs to now be cloned to your computer. You can do this by opening GitHub Desktop or Git Bash.

Clone Repository via GitHub Desktop:
   - Open GitHub Desktop and click 'Clone a repository from the internet'
   - Click URL and paste the URL into the designated box 
   - The local path is your destination folder where you will be cloning the repository to
   - Click clone and the files should now be available in your detination folder on your computer 
   
Clone Repository via GitBash:
   - Open GitBash and navigate to where your destination folder will be 
   - Enter the command line: git clone https://github.com/kirstymcl1/project 
   - Messages for downloading the files should appear and the repository should now be cloned to your computer.

After the repository has been cloned, a conda environment should now be created to work through the code. This will be done by using the environment.yml file provided in this repository. To do this, open Anaconda Navigator and go to the Environments tab. From this tab, click import and search for the environment.yml file in the folder where you cloned the repository to. Give the environment a meaningful name, example: 'crimeproject'. This may take some time. 

Once this has been completed, go back to the Home tab on Anaconda Navigator and ensure that your new environment is selected instead of the deafult 'base'. You can now open jupyter notebook from this channel or open the command prompt from this environment and launch (jupyter-notebook.exe). Either route will open jupyter notebook in a webpage, which you can then navigate to your repository folder and open the NI_Crime_Project notebook to work through.
