$resourceGroup = "exam-grp"
$location = "West US 3"
$vmName="appvm"
$vmSize="Standard_DS2_v2"
$vmImage = "Win2019Datacenter"
$nsgName="app-nsg"
$virtualNetworkName="exam-network"
$subnetName="SubnetC"

# Get-AzVMSize -Location "North Europe"

New-AzResourceGroup -Name $resourceGroup -Location $location

New-AzVM -ResourceGroupName $resourceGroup -Location $location -Name $vmName -VirtualNetworkName $virtualNetworkName `
-SubnetName $subnetName -Size $vmSize -Image $vmImage -SecurityGroupName $nsgName -PublicIpAddressName $vmPublicIP `
-Credential (Get-Credential)

