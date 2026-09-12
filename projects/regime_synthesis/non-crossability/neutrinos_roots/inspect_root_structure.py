import uproot

file = uproot.open("EnerySpectrum.root")

print(file.keys())