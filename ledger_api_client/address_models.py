from ledger_api_client.abstract_address_models import AbstractUserAddress

#if not is_model_registered('address', 'UserAddress'):
class UserAddress(AbstractUserAddress):
    pass

    class Meta:
         managed = False
         db_table = 'address_useraddress'

