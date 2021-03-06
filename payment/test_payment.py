import os
import string
import time

import pytest

from jumpscale.loader import j

WALLET_NAME = os.environ.get("WALLET_NAME")
WALLET_SECRET = os.environ.get("WALLET_SECRET")

TRANSACTION_FEES = 0.1

zos = j.sals.zos


def check_stellar():
    try:
        j.tools.http.get("https://testnet.threefold.io/threefoldfoundation/transactionfunding_service/fund_transaction")
    except:
        return True
    

stellar_down = pytest.mark.skipif(check_stellar(), reason="Stellar is down")

def get_funded_wallet():
    if WALLET_NAME and WALLET_SECRET:
        wallet = j.clients.stellar.get(WALLET_NAME, network="TEST", secret=WALLET_SECRET)
        return wallet
    else:
        raise ValueError("Please provide add Values to the global variables WALLET_NAME and WALLET_SECRET")


def create_new_wallet():
    wallet_name = j.data.idgenerator.nfromchoices(10, string.ascii_letters)
    wallet = j.clients.stellar.new(wallet_name, network="TEST")
    wallet.activate_through_friendbot()
    wallet.add_known_trustline("TFT")
    return wallet


def get_wallet_balance(wallet):
    coins = wallet.get_balance()
    tft_amount = [coin.balance for coin in coins.balances if coin.asset_code == "TFT"][0]
    return float(tft_amount)


def amount_paid_to_farmer(pool):
    escrow_info = pool.escrow_information
    total_amount = escrow_info.amount
    total_amount_dec = total_amount / 1e7
    return total_amount_dec


def create_extend_pool():
    pools = zos.pools.list()
    if pools:
        pool_id = pools[0].pool_id
        return zos.pools.extend(pool_id=pool_id, cu=1, su=1, currencies=["TFT"])
    else:
        return zos.pools.create(cu=1, su=1, farm="freefarm", currencies=["TFT"])


@stellar_down
def test01_create_pool_with_funded_wallet():
    """Test for creating a pool with funded wallet.

    **Test Scenario**
    #. Get wallet.
    #. Create a pool.
    #. Pay for the pool.
    #. Check that the pool has been created.
    #. Check that the token has been transfered from the wallet.
    """
    # . Get wallet.
    wallet = get_funded_wallet()
    user_tft_amount = get_wallet_balance(wallet)

    # . Create a pool.
    pool = zos.pools.create(cu=1, su=1, farm="freefarm", currencies=["TFT"])

    # . Pay for the pool.
    needed_tft_ammount = amount_paid_to_farmer(pool)
    zos.billing.payout_farmers(wallet, pool)

    time.sleep(60)
    # . Check that the pool has been created.
    pool_info = zos.pools.get(pool.reservation_id)
    assert pool_info.sus == 1
    assert pool_info.cus == 1

    # . Check that the token has been transfered from the wallet.
    current_tft_amount = get_wallet_balance(wallet)
    assert "%.5f" % (user_tft_amount - current_tft_amount) == "%.5f" % (needed_tft_ammount + TRANSACTION_FEES)

@pytest.mark.skip("https://github.com/threefoldtech/js-sdk/issues/440")
@stellar_down
def test02_extend_pool_with_funded_wallet():
    """Test for extending a pool with funded wallet.

    **Test Scenario**
    #. Get wallet.
    #. Extend an existing pool.
    #. Pay for the pool.
    #. Check that the pool has been extended.
    #. Check that the token has been transfered from the wallet.
    """
    # . Get wallet.
    wallet = get_funded_wallet()
    user_tft_amount = get_wallet_balance(wallet)

    # . Extend an existing pool.
    pools = zos.pools.list()
    assert pools, "There is no existing pools to be extend"

    pool_info = pools[-1]
    exist_cus = pool_info.cus
    exist_sus = pool_info.sus
    pool = zos.pools.extend(pool_id=pool_info.pool_id, cu=1, su=1, currencies=["TFT"])

    # . Pay for the pool.
    needed_tft_ammount = amount_paid_to_farmer(pool)
    zos.billing.payout_farmers(wallet, pool)

    time.sleep(60)
    # . Check that the pool has been extended.
    pool_info = zos.pools.get(pool_info.pool_id)
    assert (pool_info.sus - exist_sus) == 1
    assert (pool_info.cus - exist_cus) == 1

    # . Check that the token has been transfered from the wallet.
    current_tft_amount = get_wallet_balance(wallet)
    assert "%.5f" % (user_tft_amount - current_tft_amount) == "%.5f" % (needed_tft_ammount + TRANSACTION_FEES)


@stellar_down
def test03_create_pool_with_empty_wallet():
    """Test for creating a pool with empty wallet.

    **Test Scenario**
    #. Create empty wallet.
    #. Create a pool.
    #. Pay for the pool, should fail.
    #. Check that the pool has been created with empty units.
    """
    # . Create empty wallet.
    wallet = create_new_wallet()

    # . Create a pool.
    pool = zos.pools.create(cu=1, su=1, farm="freefarm", currencies=["TFT"])

    # . Pay for the pool, should fail.
    with pytest.raises(Exception) as e:
        zos.billing.payout_farmers(wallet, pool)
        assert e.value.status == 400
        assert e.value.title == "Transaction Failed"

    time.sleep(60)
    # . Check that the pool has been created with empty units.
    pool_info = zos.pools.get(pool.reservation_id)
    assert pool_info.sus == 0
    assert pool_info.cus == 0


@stellar_down
def test04_extend_pool_with_empty_wallet():
    """Test for extending a pool with empty wallet.

    **Test Scenario**
    #. Create empty wallet.
    #. Extend existing pool.
    #. Pay for the pool, should fail.
    #. Check that the pool has not been extended.
    """
    # . Create empty wallet.
    wallet = create_new_wallet()

    # . Extend an existing pool.
    pools = zos.pools.list()
    assert pools, "There is no existing pools to be extended"

    pool_info = pools[-1]
    exist_cus = pool_info.cus
    exist_sus = pool_info.sus
    pool = zos.pools.extend(pool_id=pool_info.pool_id, cu=1, su=1, currencies=["TFT"])

    # . Pay for the pool, should fail.
    with pytest.raises(Exception) as e:
        zos.billing.payout_farmers(wallet, pool)
        assert e.value.status == 400
        assert e.value.title == "Transaction Failed"

    time.sleep(60)
    # . Check that the pool has not been extended.
    pool_info = zos.pools.get(pool_info.pool_id)
    assert (pool_info.sus - exist_sus) == 0
    assert (pool_info.cus - exist_cus) == 0
