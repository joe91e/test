# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|
    config.vm.define 'sandbox' do |sandbox|
        sandbox.vm.box = "ubuntu/trusty64"

        # @todo Read this from a config file perhaps?
        sandbox.vm.network "forwarded_port", guest: 8000, host: 5000
        sandbox.vm.network "forwarded_port", guest: 8080, host: 8080
        sandbox.vm.network "forwarded_port", guest: 27017, host: 5001
        sandbox.vm.network "forwarded_port", guest: 28017, host: 5002
        sandbox.vm.network "forwarded_port", guest: 6379, host: 5003
        #sandbox.vm.network "forwarded_port", guest: 9000, host: 9000

        # Bootstrap the vm
        sandbox.vm.provision "shell", path: "provision/bootstrap.sh"
    end

    #config.vm.synced_folder "sandbox/", "/vagrant/sandbox/"
end
