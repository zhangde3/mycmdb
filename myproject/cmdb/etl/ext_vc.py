import logging
from logging.config import fileConfig
from models import VC
import configparser
import argparse

fileConfig('logger_config.ini')
logger = logging.getLogger('infoLogger')


def ext(vc_host, vc_user, vc_passwd, vc_port):

    vc = VC(host, user, passwd, port)
    logger.info("start extract %s" % )

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


def to_json():
    logger.info("start dump to json")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--host")
    args = parser.parse_args()

    if args.host and args.user and args.passwd and args.port:
        cfg = configparser.ConfigParser()
        cfg.read("config/config.ini")
        config_item = args.host
        (host, user, passwd, port) = (cfg.get(config_item, "host"), cfg.get(
            config_item, "user"), cfg.get(config_item, "passwd"), cfg.get(config_item, "port"))
        vc_objects = ext(host, user, passwd, port)
        server_list = vc_objects.get('server_list')

        logging.debug("******** %s server_list ************" % args.host)
        logging.debug(server_list)
        logging.debug(len(server_list))
