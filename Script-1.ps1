$resourceGroup = "test"
$location = "West US"
$vmName="appvm"
$vmSize="Standard_DS2_v2"
$vmImage = "Debian"
$virtualNetworkName="app-network"
$subnetName="SubnetA"
$Addressprefix="10.0.0.0/16"
$subnetAddressPrefix = "10.0.0.0/24"
$publicIPAddressName="app-public-ip"
$networkSecurityGroupName = "app-nsg"
$ipallocation = "Dynamic"

$location2 = "East US"
$vmName2="appvm2"
$virtualNetworkName2="app-network2"
$subnetName2="SubnetB"
$Addressprefix2="10.1.0.0/16"
$subnetAddressPrefix2 = "10.1.0.0/24"
$publicIPAddressName2="app-public-ip2"
$networkSecurityGroupName2 = "app-nsg2"


#Creating VM1

New-AzResourceGroup -Name $resourceGroup -Location $location

New-AzVM -ResourceGroupName $resourceGroup -Location $location2 -Name $vmName2 -VirtualNetworkName $virtualNetworkName2 `
-AddressPrefix $Addressprefix -SubnetName $subnetName -SubnetAddressPrefix $subnetAddressPrefix -Size $vmSize -Image $vmImage `
-SecurityGroupName $networkSecurityGroupName -PublicIpAddressName $publicIPAddressName -AllocationMethod $ipallocation `
-Credential (Get-Credential)


#Creating VM2

New-AzVM -ResourceGroupName $resourceGroup -Location $location -Name $vmName -VirtualNetworkName $virtualNetworkName `
-AddressPrefix $Addressprefix2 -SubnetName $subnetName2 -SubnetAddressPrefix $subnetAddressPrefix2 -Size $vmSize -Image $vmImage `
-SecurityGroupName $networkSecurityGroupName2 -PublicIpAddressName $publicIPAddressName2 -AllocationMethod $ipallocation `
-Credential (Get-Credential)

