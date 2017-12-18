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


def to_json(data,filename):
    filepath = os.path.join('dump',filename)
    logger.info("start dump to json: %s" % filepath)
    with open(filepath,'w') as wf:
        wf.write(json.dumps(data))


def ftp_upload(filename,host='csftp',user='ppa',passwd='ppa',remotedir='/zhangde3/mycmdb_dump'):
    ftp = FTP()
    ftp.connect(host, port=21)
    ftp.login(user, passwd)
    bufsize = 1024
    localpath = os.path.join('dump',filename)
    remotepath = os.path.join(remotedir,filename)
    fp = open(localpath, 'rb')
    logger.info('start uploading %s to %s' % (localpath, remotepath))
    ftp.storbinary('STOR ' + remotepath, fp, bufsize)
    ftp.set_debuglevel(0)
    fp.close()
    logger.info('done')


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

        logging.debug("******** %s server_list ************" % args.host)
        logging.debug(len(server_list))

        logging.debug("******** %s vm_list ************" % args.host)
        logging.debug(len(vm_list))

        logging.debug("******** %s ds_list ************" % args.host)
        logging.debug(len(ds_list))

        logging.debug("******** %s license_list ************" % args.host)
        logging.debug(len(license_list))

        opt_time = time.strftime('%Y%m%d',time.localtime(time.time()))

        to_json(server_list,"server_list_%s_%s.json" % (args.host, opt_time))
        to_json(vm_list,"vm_list_%s_%s.json" % (args.host, opt_time))
        to_json(ds_list,"ds_list_%s_%s.json" % (args.host, opt_time))
        to_json(license_list,"license_list_%s_%s.json" % (args.host, opt_time))

        logging.debug("******** uploading %s dumpfile to csftp ************" % (args.host))
        logging.debug(len(license_list))

        ftp_upload("server_list_%s_%s.json" % (args.host, opt_time))
        ftp_upload("vm_list_%s_%s.json" % (args.host, opt_time))
        ftp_upload("ds_list_%s_%s.json" % (args.host, opt_time))
        ftp_upload("license_list_%s_%s.json" % (args.host, opt_time))
