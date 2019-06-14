from django.shortcuts import render
from Backend import backend 

def hello(request):
   IPs = []
   IPs.append("192.168.1.41")
   IPs.append("192.168.1.41")

   disk = []
   disk.append(backend.getDiskUsage("192.168.1.41"))
   disk.append(backend.getDiskUsage("192.168.1.41"))
   ram = []
   ram.append(backend.getRamUsage("192.168.1.41"))
   ram.append(backend.getRamUsage("192.168.1.41"))
   return render(request, "bootstrap/index.html", {'disk' : disk, 'ram': ram, "IPs" : IPs})
