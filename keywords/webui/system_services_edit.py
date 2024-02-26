import xpaths
from helper.webui import WebUI
from keywords.api.post import API_POST
from keywords.api.put import API_PUT
from keywords.webui.common import Common as COM
from keywords.webui.system_services import System_Services as SERV

services_list = ['ftp', 'iscsi', 'nfs', 'smart', 'smb', 'snmp', 'ssh', 'ups']
ftp_fields = ['General Options', 'port', 'clients', 'ipconnections', 'loginattempt', 'timeout-notransfer', 'timeout']
iscsi_fields = ['Global Configuration', 'basename', 'isns-servers', 'pool-avail-threshold', 'listen-port']
nfs_fields = ['General Options', 'bindip', 'servers', 'NFSv4', 'protocols', 'v-4-v-3-owner', 'v-4-krb', 'Ports',
              'mountd-port', 'rpcstatd-port', 'rpclockd-port', 'Other Options', 'udp', 'allow-nonroot',
              'userd-manage-gids']
smart_fields = ['General Options', 'interval', 'powermode', 'difference', 'informational', 'critical']
smb_fields = ['NetBIOS', 'netbiosname', 'netbiosalias', 'workgroup', 'description', 'enable-smb-1', 'ntlmv-1-auth']
snmp_fields = ['General Options', 'location', 'contact', 'community', 'Other Options', 'options', 'zilstat', 'loglevel',
               'SNMP v3 Options', 'v-3']
ssh_fields = ['General Options', 'tcpport', 'password-login-groups', 'passwordauth', 'kerberosauth', 'tcpfwd']
ups_fields = ['General Options', 'identifier', 'mode', 'driver', 'port', 'Shutdown', 'shutdown', 'shutdowntimer',
              'shutdowncmd', 'powerdown', 'Other Options', 'nocommwarntime', 'hostsync', 'description', 'options',
              'optionsupsd', 'Monitor', 'monuser', 'monpwd', 'extrausers', 'rmonitor']


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

    @classmethod
    def verify_edit_service_ui_buttons(cls, service: str):
        buttons = ''
        assert COM.is_visible(xpaths.common_xpaths.button_field('save'))
        match service:
            case "snmp":
                assert COM.is_visible(xpaths.common_xpaths.button_field('cancel'))
                buttons = 'save and cancel'
            case "ftp":
                assert COM.is_visible(xpaths.common_xpaths.button_field('cancel'))
                assert COM.is_visible(xpaths.common_xpaths.button_field('toggle-advanced-options'))
                buttons = 'save, cancel and advanced options'
            case "ftp_adv":
                assert COM.is_visible(xpaths.common_xpaths.button_field('cancel'))
                assert COM.is_visible(xpaths.common_xpaths.button_field('toggle-advanced-options'))
                buttons = 'save, cancel and basic options'
            case "iscsi":
                buttons = 'save'
            case "s.m.a.r.t." | 'smart':
                buttons = 'save'
            case "nfs":
                buttons = 'save'
            case "ups":
                assert COM.is_visible(xpaths.common_xpaths.button_field('cancel'))
                buttons = 'save and cancel'
            case "smb":
                assert COM.is_visible(xpaths.common_xpaths.button_field('cancel'))
                assert COM.is_visible(xpaths.common_xpaths.button_field('toggle-advanced-settings'))
                buttons = 'save, cancel and advanced settings'
            case "smb_adv":
                assert COM.is_visible(xpaths.common_xpaths.button_field('cancel'))
                assert COM.is_visible(xpaths.common_xpaths.button_field('toggle-advanced-settings'))
                buttons = 'save, cancel and basic settings'
            case "ssh":
                assert COM.is_visible(xpaths.common_xpaths.button_field('cancel'))
                assert COM.is_visible(xpaths.common_xpaths.button_field('toggle-advanced-options'))
                buttons = 'save, cancel and advanced options'
        print("@@@@ service buttons: " + buttons)

    # @classmethod
    # def assert_edit_service_ui(service: str):
    #     status = true
    #     fieldname = ""
    #     for (string key : servicefields.keyset()):
    #         match key:
    #             # @@@@ section titles @@@@
    #             # ftp_adv
    #             case "access":
    #             # ftp_adv
    #             case "bandwidth":							// ftp_adv
    #             case "general options":						// ftp, ftp_adv, nfs, smart, snmp, ssh, ups
    #             case "global configuration":				// iscsi
    #             case "monitor":								// ups
    #             case "netbios":								// smb
    #             case "nfsv4":								// nfs
    #             case "other options":						// ftp_adv, nfs, smb_adv, snmp, ups
    #             case "ports":								// nfs
    #             case "shutdown":							// ups
    #             case "snmp v3 options":						// snmp
    #             case "tls":									// ftp_adv
    #                 testobj = findtestobject('webui/common_objects/legend_title',[('title'):servicefields.get(key)])
    #                 fieldname = 'section title'
    #                 break
    #             # @@@@ dropdown fields @@@@
    #             case "bind interfaces":						// ssh_adv
    #             case "bind ip addresses":					// nfs, smb_adv
    #             case "enabled protocols":					// nfs
    #             case "guest account":						// sbm_adv
    #             case "log level":							// smb_adv, snmp
    #             case "power mode":							// smart
    #             case "sftp log level":						// ssh_adv
    #             case "shutdown mode":						// ups
    #             case "unix charset":						// sbm_adv
    #             case "ups mode":							// ups
    #             case "weak ciphers":						// ssh_adv
    #                 testobj = findtestobject('webui/common_objects/select_field',[('field'):servicefields.get(key)])
    #                 fieldname = 'dropdown field'
    #                 break
    #             # @@@@ checkbox fields @@@@
    #             case "allow anonymous login":				// ftp_adv
    #             case "allow kerberos authentication":		// ssh
    #             case "allow local user login":				// ftp_adv
    #             case "allow non-root mount":				// nfs
    #             case "allow password authentication":		// ssh
    #             case "allow root login":					// ftp_adv
    #             case "allow tcp port forwarding":			// ssh
    #             case "allow transfer resumption":			// ftp_adv
    #             case "always chroot":						// ftp_adv
    #             case "compress connections":				// ssh_adv
    #             case "enable apple smb2/3 protocol extensions":	// sbm_adv
    #             case "enable fxp":							// ftp_adv
    #             case "enable smb1 support":					// smb
    #             case "enable tls":							// ftp_adv
    #             case "group directory execute":				// ftp_adv
    #             case "group directory read":				// ftp_adv
    #             case "group directory write":				// ftp_adv
    #             case "group file execute":					// ftp_adv
    #             case "group file read":						// ftp_adv
    #             case "group file write":					// ftp_adv
    #             case "local master":						// sbm_adv
    #             case "nfsv3 ownership model for nfsv4":		// nfs
    #             case "ntlmv1 auth":							// smb
    #             case "other directory execute":				// ftp_adv
    #             case "other directory read":				// ftp_adv
    #             case "other directory write":				// ftp_adv
    #             case "other file execute":					// ftp_adv
    #             case "other file read":						// ftp_adv
    #             case "other file write":					// ftp_adv
    #             case "perform reverse dns lookups":			// ftp_adv
    #             case "power off ups":						// ups
    #             case "remote monitor":						// ups
    #             case "require ident authentication":		// ftp_adv
    #             case "require kerberos for nfsv4":			// nfs
    #             case "serve udp nfs clients":				// nfs
    #             case "snmp v3 support":						// snmp
    #             case "support >16 groups":  				// nfs
    #             case "use syslog only":						// sbm_adv
    #             case "user directory execute":				// ftp_adv
    #             case "user directory read":					// ftp_adv
    #             case "user directory write":				// ftp_adv
    #             case "user file execute":					// ftp_adv
    #             case "user file read":						// ftp_adv
    #             case "user file write":						// ftp_adv
    #             case "zilstat":								// snmp
    #             //					testobj = findtestobject('webui/common_objects/checkbox_field',[('field'):servicefields.get(key)])
    #                 fieldname = 'checkbox field'
    #                 def index = 1
    #                 if(key.startswith("user directory") || key.startswith("group directory") || key.startswith("other directory")) {
    #                     index = 2
    #                 }
    #                 if(key.startswith("user ") || key.startswith("group ") || key.startswith("other ")) {
    #                     testobj = findtestobject('webui/any_xpath',[('xpath'):"(//*[@data-test='checkbox-"+servicefields.get(key)+"'])["+index+"]"])
    #                 }
    #                 break
    #             # @@@@ input fields @@@@
    #             case "administrators group":				// sbm_adv
    #             case "anonymous user download bandwidth":	// ftp_adv
    #             case "anonymous user upload bandwidth":		// ftp_adv
    #             case "base name":							// iscsi
    #             case "check interval":						// smart
    #             case "clients":								// ftp
    #             case "community":							// snmp
    #             case "connections":							// ftp
    #             case "contact":								// snmp
    #             case "critical":							// smart
    #             case "description":							// smb, ups
    #             case "difference":							// smart
    #             case "directory mask":						// sbm_adv
    #             case "driver":								// ups
    #             case "file mask":							// sbm_adv
    #             case "host sync":							// ups
    #             case "identifier":							// ups
    #             case "informational":						// smart
    #             case "iscsi listen port":					// iscsi
    #             case "isns servers":						// iscsi
    #             case "local user download bandwidth":		// ftp_adv
    #             case "local user upload bandwidth:":		// ftp_adv
    #             case "location":							// snmp
    #             case "login attempts":						// ftp
    #             case "masquerade address":					// ftp_adv
    #             case "maximum passive port":				// ftp_adv
    #             case "minimum passive port":				// ftp_adv
    #             case "monitor password":					// ups
    #             case "monitor user":						// ups
    #             case "mountd(8) bind port":					// nfs
    #             case "netbios alias":						// smb
    #             case "netbios name":						// smb
    #             case "no communication warning time":		// ups
    #             case "notransfer timeout":					// ftp
    #             case "number of threads":					// nfs
    #             case "password login groups":				// ssh
    #             case "pool available space threshold (%)":	// iscsi
    #             case "port or hostname":					// ups
    #             case "port":								// ftp
    #             case "rpc.lockd(8) bind port":				// nfs
    #             case "rpc.statd(8) bind port":				// nfs
    #             case "shutdown command":					// ups
    #             case "shutdown timer":						// ups
    #             case "tcp port":							// ssh
    #             case "timeout":								// ftp
    #             case "workgroup":							// smb
    #                 testobj = findtestobject('webui/common_objects/input_field',[('field'):servicefields.get(key)])
    #                 fieldname = 'input field'
    #                 break
    #             # @@@@ textarea fields @@@@
    #             case "additional parameters":				// ftp_adv, smb_adv, ssh_adv
    #             case "auxiliary parameters (ups.conf)":		// ups
    #             case "auxiliary parameters (upsd.conf)":	// ups
    #             case "auxiliary parameters":				// snmp
    #             case "display login":						// ftp_adv
    #             case "extra users":							// ups
    #                 testobj = findtestobject('webui/common_objects/textarea_field',[('field'):servicefields.get(key)])
    #                 fieldname = 'textarea field'
    #                 break
    #             default :
    #                 break

# 	// verify tabs if they exist
# 	if (service == "iscsi") {
# 		if (assert_edit_service_ui_tabs(globalvariable.edit_iscsi_tabs) == false) {
# 			status = false
# 		}
# 	}
#
# 	// verify buttons if they exist
# 	if (assert_edit_service_ui_buttons(service) == false) {
# 		status = false
# 	}
#
# 	// verify advanced settings ui
# 	if (assert_advanced_settings_ui(service) == false) {
# 		status = false
# 	}
#
# 	return status
# }
