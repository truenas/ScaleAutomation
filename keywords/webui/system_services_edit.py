import xpaths
from helper.webui import WebUI
from keywords.api.post import API_POST
from keywords.api.put import API_PUT
from keywords.webui.common import Common as COM
from keywords.webui.system_services import System_Services as SERV


services_list = ['ftp', 'iscsi', 'nfs', 'smart', 'smb', 'snmp', 'ssh', 'ups']
ftp_fields = ['General Options', 'port', 'clients', 'ipconnections', 'loginattempt', 'timeout-notransfer', 'timeout']
iscsi_fields = ['Global Configuration', 'basename', 'isns-servers', 'pool-avail-threshold', 'listen-port']
nfs_fields = ['General Options', 'bindip', 'servers', 'NFSv4', 'protocols', 'v-4-v-3-owner', 'v-4-krb', 'Ports', 'mountd-port', 'rpcstatd-port', 'rpclockd-port', 'Other Options', 'udp', 'allow-nonroot', 'userd-manage-gids']
smart_fields =['General Options', 'interval', 'powermode', 'difference', 'informational', 'critical']
smb_fields = ['NetBIOS', 'netbiosname', 'netbiosalias', 'workgroup', 'description', 'enable-smb-1', 'ntlmv-1-auth']
snmp_fields = ['General Options', 'location', 'contact', 'community', 'Other Options', 'options', 'zilstat', 'loglevel', 'SNMP v3 Options', 'v-3']
ssh_fields = ['General Options', 'tcpport', 'password-login-groups', 'passwordauth', 'kerberosauth', 'tcpfwd']
ups_fields = ['General Options', 'identifier', 'mode', 'driver', 'port', 'Shutdown', 'shutdown', 'shutdowntimer', 'shutdowncmd', 'powerdown', 'Other Options', 'nocommwarntime', 'hostsync', 'description', 'options', 'optionsupsd', 'Monitor', 'monuser', 'monpwd', 'extrausers', 'rmonitor']


class System_Services_Edit:
    @classmethod
    def click_edit_button_by_servicename(cls, servicename: str):
        name = SERV.return_backend_service_name(servicename)
        COM.click_button(f'{name}-edit')
        WebUI.wait_until_visible(xpaths.common_xpaths.any_header(servicename, 3))

    @classmethod
    def verify_edit_button_visible_by_servicename(cls, servicename: str):
        name = SERV.return_backend_service_name(servicename)
        assert COM.is_visible(xpaths.common_xpaths.button_field(f'{name}-edit'))

