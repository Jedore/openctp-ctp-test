import importlib
from queue import Queue

import pytest

Q_CONNECT = Queue(maxsize=1)
Q_AUTH = Queue(maxsize=1)

TIMEOUT = 5  # seconds

USER = '209025'

from openctp_ctp_CTP_VERSION import tdapi as api


class CTdSpiImpl(api.CThostFtdcTraderSpi):
    def __init__(self, tdapi):
        super().__init__()
        self.tdapi = tdapi

    def OnFrontConnected(self):
        Q_CONNECT.put(True, timeout=TIMEOUT)
        req = api.CThostFtdcReqAuthenticateField()
        req.BrokerID = '9999'
        req.UserID = USER
        req.AppID = 'simnow_client_test'
        req.AuthCode = '0000000000000000'
        self.tdapi.ReqAuthenticate(req, 0)

    def OnRspAuthenticate(self, pRspAuthenticateField: api.CThostFtdcRspAuthenticateField,
                          pRspInfo: api.CThostFtdcRspInfoField, nRequestID: int, bIsLast: bool):
        if pRspInfo is None or pRspInfo.ErrorID == 0:
            # success
            Q_AUTH.put(True, timeout=TIMEOUT)
        else:
            # failed
            Q_AUTH.put(False, timeout=TIMEOUT)


def test_tdapi():
    # Success if at least 1 md front success.
    td_fronts = (
        'tcp://180.168.146.187:10130',
        'tcp://180.168.146.187:10201',
        'tcp://180.168.146.187:10202',
        'tcp://180.168.146.187:10203',
    )
    error = None
    for td_front in td_fronts:
        try:
            tdapi = api.CThostFtdcTraderApi.CreateFtdcTraderApi(USER)

            assert 'CTP_VERSION2' in tdapi.GetApiVersion(), 'GetApiVersion Failed!'

            tdspi = CTdSpiImpl(tdapi)
            tdapi.RegisterSpi(tdspi)
            tdapi.RegisterFront(td_front)
            tdapi.Init()

            try:
                Q_CONNECT.get(timeout=TIMEOUT)
            except:
                assert False, 'Connect Failed!'

            try:
                if not Q_AUTH.get(timeout=TIMEOUT):
                    assert False, 'Auth Failed!'

            except:
                assert False, 'Auth Failed!'

            # success
            break
        except AssertionError as e:
            error = str(e)
    else:
        assert False, error
