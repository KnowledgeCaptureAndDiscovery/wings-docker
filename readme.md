# WINGS-Docker repository

This repository contains different WINGS docker images with pre-installed software, as well as the instructions to run them.

* kcapd/wings-base: Clean installation of WINGS and Docker. 
* kcapd/wings-genomics: contains all the software from wings-base plus python-dev, samtools, tophat, cufflinks, RSeQC and R.

In order to use this images, you can simply pull them from dockerhub: 

```docker pull kcapd/wings-base``` or ```docker pull kcapd/wings-genomics```


Alternatively, you may build any of the docker files in the "docker" folder of this repository. Please build them from the folder whichc contains this readme. For example:

```docker build -t [IMAGE_NAME] -f docker/default/Dockerfile . ```

Note that this takes a little bit more time than simply pulling the images from dockerhub. However, this approach is better if you want to install additional software on your WINGS image.

## Executing WINGS:

Once you have pulled or created your images, you should run the file ```start-wings.sh``` that you will find on the "scripts" folder of this repository: 

```bash
# If [NAME] is not specified, it defaults to wings.
./start-wings.sh [NAME]
```

This file will execute the container with the following options (it is assumed that the image name is kcapd/wings-base):

```bash
docker run --interactive \
               --tty \
               --env WINGS_MODE='dind' \
               --volume "${NAME}_vol":/opt/wings \
               --name ${NAME} \
               --publish 8080:8080 \
               ${ARGS} kcapd/wings-base
```

And now you can access WINGS' web interface from the Docker image: ```http://localhost:8080/wings-portal```

If you want to stop the WINGS container, execute the following command:

```bash
docker stop kcapd/wings-base
```

If you start and stop your container several times, sometimes the volume is not mounted correctly and leads to errors. In those cases you should remove your volume: 

```bash
docker volume rm wings_vol
```
And call the ```start-wings.sh``` script again

**Attention: If you remove the volume, you will delete the data, workflows and executions created on the container.** We recommend that you copy all the storage data befor that. In order to do that, you should mount a volume (see below).

### Copy results from different executions into your local computer

You can access the results from your workflows, using the web browser: ```http://localhost:8080/wings-portal```, going to "Analysis->Access Runs" or "Advanced ->Manage Data". Whenever a file is downloaded, it will be saved to your local computer.

In order to save the results from your WINGS dockerized image, you have to **mount another volume**. The volume will be used to copy the results of the workflow to your localhost computer:

1.	Edit the ```start-wings.sh``` script adding another volume after the ```--volume "${NAME}_vol":/opt/wings \``` line: 

```bash
--volume "c:/Users/dgarijo/Desktop/sharedFolder":/out \
```
In the tutorial we are sharing a folder on the local computer on path ```c:/Users/dgarijo/Desktop/sharedFolder```. The shared folder in the container will be called ```out```

2. Execute the ```start-wings.sh```

3. Select the folder with results that you want to copy. Unless the Dockerfile is changed, it should be on 
```
cd /opt/wings/storage/default/users/username/domain/
```
4. Copy the results you want to the mounted volume: 
```
cp /opt/wings/storage/default/users/admin/blank/data/out1.txt /out/out1.txt
```

Those result will appear on your shared folder.
