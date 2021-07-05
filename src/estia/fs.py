"""
    Interacting with the IPFS API. 
"""
import os
import ipfshttpclient

# Huge thanks to Minty for the original implementation: https://github.com/yusefnapora/minty

with ipfshttpclient.connect() as client:
	hash = client.add('test.txt')['Hash']
	print(client.stat(hash))
    

class IpfsInterface:
    
    def createNFTFromData(content, options):
        """Create an NFT from the given data
        options is a dict:
        options = {
            "path":"/some/path" - optional file path to set when storing the data on IPFS
            "name":"some" - optional name to set in NFT metadata
            "description":"something" - optional description to store in NFT metadata
            "owner":"ethaddress" - required: ethereum address that should own the new NFT.
        }
        content is a Buffer of data (e.g, image, text, blob etc) 
        """
        # adding asset to IPFS
        file_path = options.filepath
        basename = os.path.splitext(file_path)

        # When adding an object to IPFS with directory prefix in path
        # IPFS will create directory structure. 
        # 'ipfs://QmaNZ2FCgvBPqnxtkbToVVbK2Nes6xk5K4Ns6BsmkPucAM/cat-pic.png' instead of
        # 'ipfs://QmaNZ2FCgvBPqnxtkbToVVbK2Nes6xk5K4Ns6BsmkPucAM'

        ipfs_path = "/nft/" + basename
    