import json
import logging
from logging.config import fileConfig
from models.vc import VC
import configparser
import argparse
import os
from ftplib import FTP
import socket
import time

os.chdir('/home/itop/scripts/mycmdb/myproject/cmdb/etl')

fileConfig('logger_config.ini')
logger = logging.getLogger('infoLogger')


def ext(host, user, passwd, port):
    vc = VC(host, user, passwd, port)
    logger.info("start extract %s" % host)

    vc_objects = {}
    server_list = []
    vm_list = []
    ds_list = []
    license_list = []
    for dc in vc.get_data_center_list():
        server_list += vc.get_server_list(dc)
        vm_list += vc.get_vm_list(dc)
        ds_list += vc.get_ds_list(dc)
        license_list += vc.get_license_list()

    vc_objects['server_list'] = server_list
    vc_objects['vm_list'] = vm_list
    vc_objects['ds_list'] = ds_list
    vc_objects['license_list'] = license_list

    return vc_objects


def to_json(data,filepath):
    logger.info("start dump to json: %s" % filepath)
    with open(filepath,'w') as wf:
        wf.write(json.dumps(data))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--host")
    args = parser.parse_args()

    if args.host:
        cfg = configparser.ConfigParser()
        cfg.read("config/config.ini")
        config_item = args.host
        (host, user, passwd, port) = (cfg.get(config_item, "host"), cfg.get(
            config_item, "user"), cfg.get(config_item, "passwd"), cfg.get(config_item, "port"))
        vc_objects = ext(host, user, passwd, port)

        server_list = vc_objects.get('server_list')
        vm_list = vc_objects.get('vm_list')
        ds_list = vc_objects.get('ds_list')
        license_list = vc_objects.get('license_list')

        opt_time = time.strftime('%Y%m%d',time.localtime(time.time()))
        target_dir = "/itop_data/http_dir/share/"

        server_json = "server_list_%s_%s.json" % (args.host, opt_time)
        vm_json = "vm_list_%s_%s.json" % (args.host, opt_time)
        ds_json = "ds_list_%s_%s.json" % (args.host, opt_time)
        license_json = "license_list_%s_%s.json" % (args.host, opt_time)

        to_json(server_list,os.path.join(target_dir,server_json))
        to_json(vm_list,os.path.join(target_dir,vm_json))
        to_json(ds_list,os.path.join(target_dir,ds_json))
        to_json(license_list,os.path.join(target_dir,license_json))
