# Test Case
## Prerequisites
- Centos 7.6
- 16G RAM 4vcpu 250G disk
## Software prerequisites
```bash
sudo yum install -y epel-release
sudo yum install -y ansible pyOpenSSL \
  python-cryptography python-lxml git python2-passlib \
  java-1.8.0-openjdk-headless patch httpd-tools
```
## Checkout Openshift Ansible 3.11
```bash
git clone --single-branch --branch release-3.11 \
  https://github.com/openshift/openshift-ansible.git
```
## Copy This Repository to Openshift Ansible
```bash
cd openshift-ansible
git clone --single-branch --branch openshift https://github.com/ratanovvv/testcases.git .
```
## Setup Openshift for localhost
```bash
sudo ansible-playbook -i inventory/hosts.localhost playbooks/prerequisites.yml
sudo ansible-playbook -i inventory/hosts.localhost playbooks/deploy_cluster.yml
```
Now you have working EFK. You can login through this [link](https://kibana.router.default.svc.cluster.local)
## Login to Openshift
```bash
sudo cp /etc/origin/master/admin.kubeconfig ./
sudo chown ${USER}:${USER} ./admin.kubeconfig
export KUBECONFIG=$(pwd)/admin.kubeconfig
```
## Create Elasticsearch(6.3.2) and Kibana(6.3.2) in Openshift
```bash
oc new-project custom \
    --description="custom" --display-name="custom"
oc project custom
oc create -f custom/es.yaml
oc create -f custom/es.svc.yaml
oc create -f custom/kibana.yaml
oc create -f custom/kibana.svc.yaml
```
## Apply filebeat role to send logs to Elasticsearch(6.3.2)
```bash
ansible-playbook -i inventory/hosts.localhost playbooks/filebeat-playbook.yml -b --extra-vars "elasticsearch_url=es-custom.router.default.svc.cluster.local:80"
```
## Create Postgresql and Odoo in Openshift
```bash
oc create -f custom/pg.yaml
oc create -f custom/pg.svc.yaml
oc create -f custom/odoo.yaml
oc create -f custom/odoo.svc.yaml
```
Now you see logs in EFK [here](https://kibana.router.default.svc.cluster.local) and in ELK(6.3.2) [here](http://kibana-custom.router.default.svc.cluster.local)
