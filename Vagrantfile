# -*- mode: ruby -*-
# vi: set ft=ruby :
numofnodes = 1
# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure("2") do |config|
  # The most common configuration options are documented and commented below.
  # For a complete reference, please see the online documentation at
  # https://docs.vagrantup.com.

  # Every Vagrant development environment requires a box. You can search for
  # boxes at https://vagrantcloud.com/search.
  config.vm.box = "sbeliakou/centos-7.4-x86_64-minimal"

  config.vm.provision "shell", inline: "echo Hello"

  config.vm.define "lb" do |lb|
    lb.vm.hostname = "master"
    lb.vm.network "private_network", ip: "50.50.50.49"
    lb.vm.provision "shell", path: "zab.sh"

    lb.vm.provider "virtualbox" do |vb|
  	vb.gui = false
  	vb.name = "master"
  	vb.memory = "1024"
end
  end

(1..numofnodes).each do |i|
    config.vm.define "node#{i}" do |node|
    node.vm.hostname = "node#{i}"
    node.vm.network "private_network", ip: "50.50.50.#{i+49}"
    node.ssh.insert_key = false
    node.vm.provider 'virtualbox' do |vb|
      vb.gui = false
      vb.memory= "2048"
      vb.name = "node#{i}"
    end

  node.vm.provision "shell", path: "slave.sh"
  end 
end

 
end
