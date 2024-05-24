idmap_active_directory_primary_domain = '//*[@data-test="text-name-idmap-ds-type-activedirectory-row-text"]'
"""This variable sets the xpath for the idmap active directory primary domain"""
idmap_smb_primary_domain = '//*[@data-test="text-name-idmap-ds-type-default-domain-row-text"]'
"""This variable sets the xpath for the idmap active directory primary domain"""
kerberos_keytab_ad_machine_account = '//*[@data-test="text-name-kerberos-keytab-ad-machine-account-row-text"]'
"""This variable sets the xpath for the kerberos keytab ad machine account"""


def kerberos_realm(realm_xapth: str) -> str:
    """
    This function sets the text for the given kerberos realm

    :param realm_xapth: text of the given kerberos realm
    :return: xpath string for given kerberos realm
    """
    return f'//*[@data-test="text-realm-kerberos-realm-{realm_xapth}-row-text"]'
