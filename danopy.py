import os
from bip_utils import Bip39MnemonicGenerator, Bip44Changes, CardanoShelley, Cip1852Coins, Cip1852

# Generate a random 32-byte seed
random_seed = os.urandom(32)
print("Generated random seed:", random_seed.hex())

# Create from the generated seed
cip1852_mst_ctx = Cip1852.FromSeed(random_seed, Cip1852Coins.CARDANO_ICARUS)

print("\nGenerated Seed Phrase:")
# Generate seed phrase from the random seed
seed_phrase = Bip39MnemonicGenerator().FromEntropy(random_seed)
print(seed_phrase)

print("\nMaster Keys:")
# Print master keys
print("Private Key:", cip1852_mst_ctx.PrivateKey().Raw().ToHex())
print("Public Key:", cip1852_mst_ctx.PublicKey().RawCompressed().ToHex())

# Derive account 0 keys and use it to create a Cardano Shelley object
cip1852_acc_ctx = cip1852_mst_ctx.Purpose().Coin().Account(0)
shelley_acc_ctx = CardanoShelley.FromCip1852Object(cip1852_acc_ctx)

print("\nStaking Keys:")
# Print staking keys
print("Private Key:", shelley_acc_ctx.StakingObject().PrivateKey().Raw().ToHex())
print("Public Key:", shelley_acc_ctx.StakingObject().PublicKey().RawCompressed().ToHex())
# Print staking address
print("Staking Address:", shelley_acc_ctx.StakingObject().PublicKey().ToAddress())

# Derive external chain keys
shelley_chg_ctx = shelley_acc_ctx.Change(Bip44Changes.CHAIN_EXT)

print("\nDerive External Chain Keys:")
# Staking object is available at any level and it's always the same
print("Staking Address:", shelley_chg_ctx.StakingObject().PublicKey().ToAddress())

print("\nDerive and Print First 5 Keys and Addresses:")
# Derive the first 5 keys and addresses
for i in range(5):
    shelley_addr_ctx = shelley_chg_ctx.AddressIndex(i)

    print("\nAddress", i)
    # Print keys
    print("Private Key:", shelley_addr_ctx.PrivateKeys().AddressKey().Raw().ToHex())
    print("Public Key:", shelley_addr_ctx.PublicKeys().AddressKey().RawCompressed().ToHex())
    # Print address (addr1...)
    print("Address:", shelley_addr_ctx.PublicKeys().ToAddress())
    # Print staking address (same as StakingObject)
    print("Staking Address:", shelley_addr_ctx.PublicKeys().ToStakingAddress())
    # Same as ToStakingAddress
    print("Reward Address:", shelley_addr_ctx.PublicKeys().ToRewardAddress())
