# *Libera*: Network Hypervisor for Programmable Network Virtualization in Datacenters

## Contents
+ [Introduction](#introduction)
+ [Code Changes](#changes)
+ [Install on Ubuntu 16.04](#install)

<a name="introduction"></a>
## Introduction
This documentation includes the step-by-step instructions to run and test *Libera* framework.

*Libera* is SDN-based network hypervisor that creates multiple virtual networks (VNs) for tenants. This software is developed based on OpenVirteX, which is originally developed by ONF (Open Networking Foundation). Now, OpenVirteX and *Libera* are both managed by Korea University.

<a name="changes"></a>
## Code Changes

**1)** [compile.sh](./compile.sh) including -Dhttps.protocols=SSLv3,TLSv1,TLSv1.1,TLSv1.2, because some of the Maven plugins did not support deprecated SSL protocols

**2)** [pom.xml](./pom.xml) findbugs-maven-plugin  <version>3.0.4</version> : I'm using maven 3.6, so this plugin disappears starting from the plugin version 3.0.4

**3)** [OVXPacketOut.java](./src/main/java/net/onrc/openvirtex/messages/OVXPacketOut.java): import net.onrc.openvirtex.elements.OVXmodes.OVXmodeHandler; 


<a name="install"></a>
# Install on Ubuntu 16.04

> USE A VIRTUAL MACHINE
 
# Dependencies 

### Java 7

**1)** Java Oracle 7 (v7u80)


[Oficial Repo](https://www.oracle.com/java/technologies/javase/javase7-archive-downloads.html) : Needs oracle account



[Alternative Repo](https://mega.nz/file/6j5x1QSK#nn1QjI0S9eDmNniJBmAH4-umObXrNgZ9VYO6ahhYZak): jdk-7u80-linux-x64.tar.gz


**2)** Extract


	tar -xvf jdk-7u80-linux-x64.tar.gz


**3)** Create the jvm directory and Copy Java7


	sudo mkdir -p /usr/lib/jvm
	sudo mv jdk1.7.0_80/ /usr/lib/jvm/


**4)** Define instalation priority


	sudo update-alternatives --install "/usr/bin/java" "java" "/usr/lib/jvm/jdk1.7.0_80/bin/java" 10000

	sudo update-alternatives --install "/usr/bin/javac" "javac" "/usr/lib/jvm/jdk1.7.0_80/bin/javac" 10000

	sudo update-alternatives --install "/usr/bin/javaws" "javaws" "/usr/lib/jvm/jdk1.7.0_80/bin/javaws" 10000

**5)** Set execution rights

	sudo chmod a+x /usr/bin/java
	sudo chmod a+x /usr/bin/javac
	sudo chmod a+x /usr/bin/javaws
	sudo chown -R root:root /usr/lib/jvm/jdk1.7.0_80

**6)** Check that it did not conflict with other java versions


	sudo update-alternatives --config java

	sudo update-alternatives --config javac

	sudo update-alternatives --config javaws

### Configure apache-maven
**1)** Download and extract

[Official Repo](http://ftp.unicamp.br/pub/apache/maven/maven-3/3.6.3/binaries/apache-maven-3.6.3-bin.tar.gz):  works with wget
	
	wget http://ftp.unicamp.br/pub/apache/maven/maven-3/3.6.3/binaries/apache-maven-3.6.3-bin.tar.gz

[Alternative repo](https://mega.nz/file/njp3zARb#lHRuvp1a5PALcJq3REe6ChzJl9w2HWIYT_tbZQVIZtc)

	tar -xvf apache-maven-3.6.3-bin.tar.gz


**2)** Configuration

 > Include this lines on .profile file


 	export JAVA_HOME=/usr/lib/jvm/jdk1.7.0_80/
	export PATH=$PATH:$HOME/bin:$JAVA_HOME/bin:/opt/apache-maven-3.6.3/bin
	export JRE_HOME

> and:

	source .profile



## Execute o *Libera* framework
     
  ```shell
  sh Libera/scripts/libera.sh –-db-clear	
  ```
>or

  ```shell
  sh compilable-openvirtex-Libera/scripts/libera.sh –-db-clear	
  ```


<a name="contacts"></a>
## Contacts
+ This project is a fork of [Libera Hypervisor](https://github.com/os-libera/Libera)
+ My email is nelsonpratesg@gmail.com

+ The original project is under the lead of Professor Chuck Yoo.
+ Contributors: Gyeongsik Yang, Bong-yeol Yu, Seong-Mun Kim, Heesang Jin, Wontae Jeong, Minkoo Kang, Anumeha, Yeonho Yoo
+ Mailing list: [Here](https://groups.google.com/forum/#!forum/ovx-discuss) - We share mailing list with OpenVirteX
