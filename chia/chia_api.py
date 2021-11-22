from chia.rpc.wallet_rpc_client import WalletRpcClient
from chia.util.config import load_config
from chia.util.default_root import DEFAULT_ROOT_PATH
import asyncio


async def start():
    config = load_config(DEFAULT_ROOT_PATH, "config.yaml")
    hostname = config["self_hostname"]

    wallet = await WalletRpcClient.create(self_hostname=hostname, port=9256,
                                          root_path=DEFAULT_ROOT_PATH, net_config=config)
    """Get chia balance"""
    await wallet.log_in(fingerprint=2023648112)
    balance = await wallet.get_wallet_balance(1)
    print(f'balance {balance}')

    """Create new wallet"""
    mnemonic = await wallet.generate_mnemonic()
    print(f'mnemonic {mnemonic}')
    fingerprint = await wallet.add_key(mnemonic=mnemonic)
    print(f'fingerprint {fingerprint}')
    await wallet.log_in(fingerprint=fingerprint["fingerprint"])
    address = await wallet.get_next_address(wallet_id=1, new_address=True)
    print(f'address {address}')

    """Chia transaction"""
    tr = await wallet.send_transaction(wallet_id=1, amount=1, address='some_address', fee=0.000005)
    print(f'transaction{tr}')
    await asyncio.sleep(1)

ioloop = asyncio.get_event_loop()
tasks = [ioloop.create_task(start())]
wait_tasks = asyncio.wait(tasks)
ioloop.run_until_complete(wait_tasks)
ioloop.close()