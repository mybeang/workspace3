import logging
import requests
import time
from pprint import pformat


class _REST(object):
    def __init__(self, feature, url, user, log_level=logging.INFO):
        self.logger = logging.getLogger("_REST")
        self.logger.setLevel(log_level)
        self.url = url + "/" + feature
        self.user = user

    def _gen_url(self, url, *args):
        if not args:
            return url
        else:
            url = self.url
            for arg in args:
                url += "/" + arg
            return url

    def _to_json(self, req_obj):
        self.logger.debug("=========== RESPONSE =========")
        self.logger.debug("[STATUS CODE]: {}".format(req_obj.status_code))
        try:
            data = req_obj.json()
        except:
            self.logger.debug("Message: {}".format(req_obj.text))
            data = None
        else:
            self.logger.debug("============= JSON ===========\n{}\n=============================".format(
                pformat(data, indent=2, width=80)))
        self.logger.debug("\n\n\n")
        return data

    def get(self, *args):
        url = self._gen_url(self.url, *args)
        self.logger.debug("GET: {}".format(url))
        r = requests.get(url, auth=self.user)
        data = self._to_json(r)
        return r.status_code, data

    def post(self, dict_data, *args):
        url = self._gen_url(self.url, *args) + "?appId=org.onosproject.core"
        self.logger.debug("POST: {}".format(url))
        r = requests.post(url, auth=self.user, json=dict_data)
        data = self._to_json(r)
        return r.status_code, data

    def delete(self, *args):
        url = self._gen_url(self.url, *args)
        self.logger.debug("DELETE: {}".format(url))
        r = requests.delete(url, auth=self.user)
        data = self._to_json(r)
        return r.status_code, data


class SdnController(object):
    def __init__(self, ip, user_id, user_pw, log_level=logging.INFO):
        url = "http://" + ip + ":8181/onos/v1"
        self._d_rest = _REST('devices', url, (user_id, user_pw))
        self._f_rest = _REST('flows', url, (user_id, user_pw))
        self.logger = logging.getLogger('SdnController')
        self.logger.setLevel(log_level)
        self.get_all_devices_info()
        self.get_all_flows()

    def get_all_devices_info(self):
        code, devices_data = self._d_rest.get()
        if code != "200":
            self.logger.error("Could not get the devices information")
            return
        self.devices = []
        for device_data in devices_data['devices']:
            self.devices.append({
                "device_ip": device_data['managementAddress'],
                "of_ver": device_data['protocol'],
                "device_id": device_data['id'],
            })

    def get_all_flows(self):
        code, flows_data = self._f_rest.get()
        if code != "200":
            self.logger.error("Could not get the devices information")
            return
        self.flows = []
        for flow_data in flows_data['flows']:
            data = dict()
            data.update({"device_id": flow_data['deviceId']})
            data.update({"flow_id": flow_data['id']})
            for criteria in flow_data['selector']['criteria']:
                if criteria['type'] == 'IN_PORT' and 'port' in criteria:
                    data.update({'input_port': criteria['port']})
            for instruction in flow_data['treatment']['instructions']:
                if instruction['type'] == 'OUTPUT' and 'port' in instruction:
                    data.update({'output_port': instruction['port']})
            self.flows.append(data)

    def add_flow(self, device_id, in_port, out_port):
        flow_data = {
            "flows": [
                {
                    "priority": 1,
                    "timeout": 0,
                    "isPermanent": True,
                    "deviceId": device_id,
                    "treatment": {
                        "instructions": [
                            {"type": "OUTPUT", "port": out_port}
                        ]
                    },
                    "selector": {
                        "criteria": [
                            {"type": "IN_PORT", "port": in_port}
                        ]
                    }
                }
            ]
        }
        code, data = self._f_rest.post(flow_data)
        if code != '200' or data is None or not data:
            self.logger.error('Could not add the flow entry')
            return
        will_data = {
            "device_id": device_id,
            "flow_id": data['flows'][0]['flowId'],
            "input_port": in_port,
            "output_port": out_port
        }
        self.flows.append(will_data)
        time.sleep(2)

    def del_flow(self, device_id, flow_id):
        self._f_rest.delete(device_id, flow_id)


if __name__=="__main__":
    sc = SdnController("10.55.195.24", "onos", "ektks123")
