# -*- coding: UTF-8 -*-
import glob
import heapq
import json
import operator


class Log(object):
    def __init__(self, json_str):
        self.os = json_str['os']
        self.device = json_str['device']
        self.did = json_str['did']
        self.did_type = json_str['did_type']
        self.app_name = json_str['app_name']
        self.app_version = json_str['app_version']
        self.sdk_version = json_str['sdk_version']
        self.file_size = json_str['fileSize']
        self.app_pkg = json_str['app_pkg']
        self.logs = json_str['logs']


class Crash(object):
    def __init__(self, json_str):
        self.os = json_str['os']
        self.device = json_str['device']
        self.did = json_str['did']
        self.did_type = json_str['did_type']
        self.app_name = json_str['app_name']
        self.app_version = json_str['app_version']
        self.sdk_version = json_str['sdk_version']
        self.file_size = json_str['fileSize']
        self.app_pkg = json_str['app_pkg']
        self.crashes = json_str['crash']


class LogResult(object):
    def __init__(self):
        self.count = [0]
        self.device = {}
        self.os = {}
        self.sdk_version = {}
        self.app_version = {}
        self.app_name = {}
        self.app_pkg = {}
        self.did = {}
        self.result = [[], [], [], [], [], []]
        self.file_size = []


class CrashResult(object):
    def __init__(self):
        self.count = [0]
        self.app_name = {}
        self.did = {}
        self.sdk_version = {}
        self.device = {}
        self.app_version = {}
        self.os = {}
        self.app_pkg = {}
        self.result = []


def print_statistics_result(log_data, log_result):
    print 'log记录条数', len(log_data)
    print '平均文件大小', sum(log_result.file_size) / len(log_result.file_size)
    print 'device', sorted(log_result.device.items(), key=operator.itemgetter(1), reverse=True)
    print '手机品牌型号数量', len(log_result.device.keys())
    print 'os', sorted(log_result.os.items(), key=operator.itemgetter(1), reverse=True)
    print '操作系统数量', len(log_result.os.keys())
    print 'sdk_version', sorted(log_result.sdk_version.items(), key=operator.itemgetter(1), reverse=True)
    print 'sdk版本数量', len(log_result.sdk_version.keys())
    print 'app_version', sorted(log_result.app_version.items(), key=operator.itemgetter(1), reverse=True)
    print 'app版本数量', len(log_result.app_version.keys())
    print 'app_name', log_result.app_name
    print 'app_pkg', log_result.app_pkg
    print 'did', sorted(log_result.did.items(), key=operator.itemgetter(1), reverse=True)
    print 'UV', len(log_result.did.keys()), 'PV', sum(log_result.did.values())
    print '请求成功次数', sum(log_result.result[0]), '请求失败次数', sum(log_result.result[1]), '平均请求响应时间', sum(
        log_result.result[2]) / sum(
        log_result.result[0]), '最大请求响应时间', max(log_result.result[2]), '最小请求响应时间', min(
        log_result.result[2]), '平均图片加载时间', sum(log_result.result[3]) / sum(
        log_result.result[0]), '最大图片加载时间', max(log_result.result[3]), '最小图片加载时间', min(log_result.result[3])


def print_statistics_crash(crash_data, crash_result):
    print 'crash记录条数', len(crash_data)
    print 'device', sorted(crash_result.device.items(), key=operator.itemgetter(1), reverse=True)
    print '手机品牌型号数量', len(crash_result.device.keys())
    print 'os', sorted(crash_result.os.items(), key=operator.itemgetter(1), reverse=True)
    print '操作系统数量', len(crash_result.os.keys())
    print 'sdk_version', sorted(crash_result.sdk_version.items(), key=operator.itemgetter(1), reverse=True)
    print 'sdk版本数量', len(crash_result.sdk_version.items())
    print 'app_version', sorted(crash_result.app_version.items(), key=operator.itemgetter(1), reverse=True)
    print 'app版本数量', len(crash_result.app_version.keys())
    print 'did', sorted(crash_result.did.items(), key=operator.itemgetter(1), reverse=True)
    print 'crash次数', sum(crash_result.did.values())
    print crash_result.result


def statistics_logs(log, log_result):
    try:
        log_result.device[log.device] = log_result.device.get(log.device, 0) + 1
        log_result.os[log.os] = log_result.os.get(log.os, 0) + 1
        log_result.sdk_version[log.sdk_version] = log_result.sdk_version.get(log.sdk_version, 0) + 1
        log_result.app_version[log.app_version] = log_result.app_version.get(log.app_version, 0) + 1
        log_result.app_name[log.app_name] = log_result.app_name.get(log.app_name, 0) + 1
        log_result.app_pkg[log.app_pkg] = log_result.app_pkg.get(log.app_pkg, 0) + 1
        log_result.file_size.append(log.file_size)
        for l in log.logs:
            # pv
            log_result.did[log.did] = log_result.did.get(log.did, 0) + l[2]
            if l[1] == 1:
                # 成功次数
                log_result.result[0].append(l[2])
                # 网络请求时间
                log_result.result[2].append(l[3])
                # 图片加载时间
                log_result.result[3].append(l[4])
                # 广告unit
                log_result.result[4].append(l[7])
                # 网络状态
                log_result.result[5].append(l[8])
            else:
                # 失败次数
                log_result.result[1].append(l[2])
    except ValueError:
        print ValueError
    finally:
        return


def statistics_crash(crash, crash_result):
    try:
        crash_result.device[crash.device] = crash_result.device.get(crash.device, 0) + 1
        crash_result.os[crash.os] = crash_result.os.get(crash.os, 0) + 1
        crash_result.app_name[crash.app_name] = crash_result.app_name.get(crash.app_name, 0) + 1
        crash_result.app_version[crash.app_version] = crash_result.app_version.get(crash.app_version, 0) + 1
        crash_result.sdk_version[crash.sdk_version] = crash_result.sdk_version.get(crash.sdk_version, 0) + 1
        crash_result.app_pkg[crash.app_pkg] = crash_result.app_pkg.get(crash.app_pkg, 0) + 1
        tmp = []
        for l in crash.crashes:
            crash_result.did[crash.did] = crash_result.did.get(crash.did, 0) + l[3]
            if len(crash_result.result) > 0:
                for i in xrange(0, len(crash_result.result)):
                    if crash_result.result[i][0] == l[0] and crash_result.result[i][1] == l[1]:
                        crash_result.result[i][2] += l[3]
            else:
                tmp.append([l[0], l[1], l[3]])
        for l in tmp:
            crash_result.result.append(l)
    except ValueError:
        print ValueError
    finally:
        return


def get_data_by_line(file_path, log_result, crash_result, log_data, crash_data):
    with open(file_path, 'rt') as f:
        for line in f:
            if len(line) < 300:
                continue
            try:
                data = json.loads(line)
                if 'fileSize' not in line:
                    continue
                if 'app_pkg' not in line:
                    continue
                if 'Android' in data['os']:
                    if 'logs' in data:
                        log_result.count[0] += 1
                        log = Log(data)
                        log_data.append(log)
                        statistics_logs(log, log_result)
                    if 'crash' in data:
                        crash_result.count[0] += 1
                        crash = Crash(data)
                        crash_data.append(crash)
                        statistics_crash(crash, crash_result)
            except ValueError:
                print ValueError


def search(file_name, log_result, crash_result, log_data, crash_data):
    for file_path in glob.glob(file_name):
        try:
            get_data_by_line(file_path, log_result, crash_result, log_data, crash_data)
        except ValueError:
            print ValueError
            continue


def wash_log_data(log_data, log_result, wash_log_result):
    i = int(round(len(log_result.result[2]) * 0.05, 0))
    j = set(heapq.nlargest(i, log_result.result[2]))
    k = set(heapq.nlargest(i, log_result.result[3]))
    for l in log_data:
        logs_tmp_request = set([tmp[3] for tmp in l.logs if tmp[1] == 1])
        logs_tmp_loadimg = set([tmp[4] for tmp in l.logs if tmp[1] == 1])
        if len(logs_tmp_request & j) > 0 or len(logs_tmp_loadimg & k) > 0:
            log_data.remove(l)
        else:
            statistics_logs(l, wash_log_result)


if __name__ == '__main__':
    file_name = r'/Users/tiger/pythonproject/*.log'
    log_result = LogResult()
    crash_result = CrashResult()
    log_data = []
    crash_data = []
    search(file_name, log_result, crash_result, log_data, crash_data)
    print_statistics_result(log_data, log_result)

    print '============================='
    print 'crash'
    print_statistics_crash(crash_data, crash_result)

    wash_log_result = LogResult()
    wash_log_data(log_data, log_result, wash_log_result)
    print '============================='
    print '清洗后数据'
    print_statistics_result(log_data, wash_log_result)
