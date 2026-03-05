from src import masks

CARD_NUMBER = 7000792289606361
ACCOUNT_NUMBER = 73654108430135874305

print(masks.get_mask_card_number(int(CARD_NUMBER)))
print(masks.get_mask_account(int(ACCOUNT_NUMBER)))
