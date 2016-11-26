#! /usr/bin/env python

import sys
from analyzr_core import *


class MgtPacketCounter(IPacketAnalyzer):
    MGT_TYPES_NAMES = [""] * 25
    _counter = [0] * 25

    def __init__(self):
        self.MGT_TYPES_NAMES[0] = "Association request"
        self.MGT_TYPES_NAMES[1] = "Association response"
        self.MGT_TYPES_NAMES[4] = "Probe request"
        self.MGT_TYPES_NAMES[5] = "Probe response"
        self.MGT_TYPES_NAMES[8] = "Beacon"
        self.MGT_TYPES_NAMES[11] = "Authentification"
        self.MGT_TYPES_NAMES[12] = "Deauthentification"

        print "Running MgtPacketCounter"

    def get_display_filter(self):
        return "wlan.fc.type == 0"

    def get_bpf_filter(self):
        return "type mgt"

    def analyze_packet(self, packet):
        tipe = int(packet["WLAN"].fc_subtype)
        self._counter[tipe] += 1

        sys.stdout.write("\rDeauthentification packets: " + str(self._counter[
                         12]) + " | Probe Requests: " + str(self._counter[4]) + " | Beacons: " + str(self._counter[8]))
        sys.stdout.flush()

    def on_end(self):
        for (idx, count) in enumerate(self._counter):
            if count == 0:
                continue
            print self.MGT_TYPES_NAMES[idx] + ":\t " + str(count)

mgt_type_counter = MgtPacketCounter()
core = AnalyzrCore(mgt_type_counter)
core.start()
