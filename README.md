**OddEye Proxy: Not maintained anymore, please use oe-go-proxy instead**
--------------

OddEye Proxy is a small and high performance proxy application that act as moc OddEye API server for agents running in internet restricted environments.  
It accepts requests from oe-agent, stores metrics in RabbitMQ and pushes it to real OddEye API servers. 

#### **Requirements**

* [RabbitMQ](https://www.rabbitmq.com/)
* [uWSGI](https://uwsgi-docs.readthedocs.io/en/latest/)
* [Python3 Requests](http://docs.python-requests.org/en/master/)
* [Python3 pika](https://pypi.python.org/pypi/pika)

#### **Install uWSGI**

uWSGI is available as a package in several OS/distributions, but we recommend to install it from source.
We need uWSGI with Python3 support.  

**Installation of dependencies on Debian / Ubuntu systems** 

```bash
apt-get install build-essential python3
apt-get install python3-dev
```

**Installation of dependencies on CentOS / Redhat systems** 

```bash
yum groupinstall "Development Tools"
yum install python
yum install python-devel
```

**Install uWSGI** 

From source: 
```bash
wget https://projects.unbit.it/downloads/uwsgi-lts.tar.gz
tar -zxvf uwsgi-lts.tar.gz
cd uwsgi-${VERSION}
python3 uwsgiconfig.py --build
cp uwsgi ${ODDEYE_PROXY_HOME}/sbin
```

Via `pip` 

```bash
pip3 install https://projects.unbit.it/downloads/uwsgi-lts.tar.gz
```

**Install `pika` python3 module so OddEye Proxy can connect to RabbitMQ.** 

```bash
 apt-get install python3-pika python3-pika-pool
```

Or via `pip`. 

```bash
pip3 install pika
```
#### **Install RabbitMQ**

Now we need to install RabbitMQ. If you already have RabbitMQ installation at your environment, you can skip this steps. 

**Debian / Ubuntu** 

```bash
apt-get install rabbitmq
```

**CentOS / Redhat** 
```bash
yum -y install epel-release
yum -y update
yum -y install erlang socat
wget https://www.rabbitmq.com/releases/rabbitmq-server/${VERSION}/rabbitmq-server-${VERSION}.noarch.rpm
rpm --import https://www.rabbitmq.com/rabbitmq-release-signing-key.asc
rpm -Uvh rabbitmq-server-${VERSION}.noarch.rpm
systemctl start rabbitmq-server
systemctl enable rabbitmq-server
```

**Enable RabbitMQ web console**

```bash
rabbitmq-plugins enable rabbitmq_management
```

**Create admin user** 

```bash
rabbitmqctl add_user admin StrongPassword
rabbitmqctl set_user_tags admin administrator
rabbitmqctl set_permissions -p / admin ".*" ".*" ".*"
```
You can manage RabbitMQ here : `http://Your_Server_IP:15672/`

#### **Run OddEye Proxy**

Now we need to configure OddEye Proxy. `conf/config` already ships with reasonable defaults, 
Just make sure to replace `[app]xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx` and `[uwsgi] uid/gid` with actual values. 
You can find your UID at Profile section of [OddEye Dashboard](https://app.oddeye.co/OddeyeCoconut/profile) 

```ini
[app]
url: https://api.oddeye.co/oddeye-barlus/put/tsdb
uuid: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
rabbit_host: 127.0.0.1
rabbit_port: 5672
rabbit_user: admin
rabbit_pass: admin
```

After configuring OddEye Proxy use `control.sh` to start daemons. 

```bash
${ODDEYE_PROXY_HOME}/control.sh startweb # Starts uWSGI web application 
${ODDEYE_PROXY_HOME}/control.sh startd # Starts RabbitMQ consumer and pushes queued items to OddEye API
${ODDEYE_PROXY_HOME}/control.sh startall # Starts both uWSGI and daemon 
 
${ODDEYE_PROXY_HOME}/control.sh stopweb # Stops uWSGI web application 
${ODDEYE_PROXY_HOME}/control.sh stopd # Stops RabbitMQ consumer and pushes queued items to OddEye API
${ODDEYE_PROXY_HOME}/control.sh stopall # Stops both uWSGI and daemon 
```
