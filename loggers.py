import logging
import sys


msg01 = u'\n\nDALTEST_M2400 login: \nDALTEST_M2400 login: '
msg02 = u'admin\nPassword: '
msg03 = u'\nLogin Time: Aug 03, 2001 15:47:01 (Fri) GMT \nDALTEST_M2400> '
msg04 = u'\r\nDALTEST_M2400> '
msg05 = u'\r\nDALTEST_M2400> '
msg06 = u'\r\nDALTEST_M2400> '
msg07 = u'\nUsername: '
msg08 = u'admin\nPassword: '
msg09 = u'\nLast login: Sun May  1 14:45:15 from 10.55.61.1\nveos-01>'
msg10 = u'\nveos-01>'
msg11 = u'\nveos-01>'
msg12 = u'\nveos-01>'
msg13 = u'\nIOSXE-02#\nIOSXE-02#'
msg14 = u'\nIOSXE-02#'
msg15 = u'\nIOSXE-02#'
msg16 = u'\nIOSXE-02#'
msg17 = u'enable\r\nDALTEST_M2400# '
msg18 = u'\r\nDALTEST_M2400# '
msg19 = u'\r\nDALTEST_M2400# '
msg20 = u'show version\nCisco IOS XE Software, Version 03.16.00.S - Extended Support Release\nCisco IOS Software, CSR1000V Software (X86_64_LINUX_IOSD-UNIVERSALK9-M), Version 15.5(3)S, RELEASE SOFTWARE (fc6)\nTechnical Support: http://www.cisco.com/techsupport\nCopyright (c) 1986-2015 by Cisco Systems, Inc.\nCompiled Sun 26-Jul-15 20:16 by mcpre\n\n\nCisco IOS-XE software, Copyright (c) 2005-2015 by cisco Systems, Inc.\nAll rights reserved.  Certain components of Cisco IOS-XE software are\nlicensed under the GNU General Public License ("GPL") Version 2.0.  The\nsoftware code licensed under GPL Version 2.0 is free software that comes\nwith ABSOLUTELY NO WARRANTY.  You can redistribute and/or modify such\nGPL code under the terms of GPL Version 2.0.  For more details, see the\ndocumentation or "License Notice" file accompanying the IOS-XE software,\nor the applicable URL provided on the flyer accompanying the IOS-XE\nsoftware.\n\n\nROM: IOS-XE ROMMON\n\nIOSXE-02 uptime is 5 weeks, 3 days, 4 hours, 5 minutes\nUptime for this control processor is 5 weeks, 3 days, 4 hours, 7 minutes\nSystem returned to ROM by reload\nSystem restarted at 02:51:19 UTC Tue Apr 30 2019\nSystem image file is "bootflash:packages.conf"\nLast reload reason: Reload Command\n\n\n\nThis product contains cryptographic features and is subject to United\nStates and local country laws governing import, export, transfer and\nuse. Delivery of Cisco cryptographic products does not imply\nthird-party authority to import, export, distribute or use encryption.\nImporters, exporters, distributors and users are responsible for\ncompliance with U.S. and local country laws. By using this product you\nagree to comply with applicable laws and regulations. If you are unable\nto comply with U.S. and local laws, return this product immediately.\n\nA summary of U.S. laws governing Cisco cryptographic products may be found at:\nhttp://www.cisco.com/wwl/export/crypto/tool/stqrg.html\n\nIf you require further assistance please contact us by sending email to\nexport@cisco.com.\n\nLicense Level: ax\nLicense Type: Default. No valid license found.\nNext reload license Level: ax\n\ncisco CSR1000V (VXE) processor (revision VXE) with 1095671K/6147K bytes of memory.\nProcessor board ID 9PTNEZKBWF6\n8 Gigabit Ethernet interfaces\n32768K bytes of non-volatile configuration memory.\n3022152K bytes of physical memory.\n1482751K bytes of virtual hard disk at bootflash:.\n\nConfiguration register is 0x2102\n\nIOSXE-02#'


msgs_0_0 = [msg01, msg02, msg03, msg04, msg05, msg06]
msgs_1_0 = [msg07, msg08, msg09, msg10, msg11, msg12]
msgs_2_0 = [msg13, msg14, msg15, msg16]
msgs_0_1 = [msg17, msg18, msg19]
msgs_2_1 = [msg20]


class Session(object):
    def __init__(self):
        self.logger = logging.getLogger(str(id(self)))

    def pr_logs(self, text):
        self.logger.info("{}: {}".format(str(id(self)), text))


class Dut(object):
    def __init__(self, name):
        self.name = name
        self.session = list()

    def create_session(self):
        self.session.append(Session())



class DCA(object):
    def __init__(self, dut_name):
        self.dut = Dut(dut_name)
        self.dut.create_session()
        self.dut.session[0].logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)-15s %(message)s')
        stdoutHandler = logging.StreamHandler(sys.stdout)
        stdoutHandler.setFormatter(formatter)
        self.dut.session[0].logger.addHandler(stdoutHandler)


class DCAS(object):
    def __init__(self, dut_names):
        self.dca = list()
        for dut_name in dut_names:
            self.dca.append(DCA(dut_name))


dut_names = ['M2400_02', 'ARISTA_01', 'IOSXE_02']
dcas = DCAS(dut_names)

for text in msgs_0_0:
    dcas.dca[0].dut.session[0].pr_logs(text)
for text in msgs_1_0:
    dcas.dca[1].dut.session[0].pr_logs(text)
for text in msgs_2_0:
    dcas.dca[2].dut.session[0].pr_logs(text)
for text in msgs_0_1:
    dcas.dca[0].dut.session[0].pr_logs(text)
for text in msgs_2_1:
    dcas.dca[2].dut.session[0].pr_logs(text)

