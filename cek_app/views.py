from asyncio.windows_events import NULL
from django.shortcuts import render
import psutil
import time
from psutil._common import bytes2human
from .forms import CommandForm
from .models import viewer_cmd
import subprocess
from django.http import HttpResponse
import ctypes
### Cached Bulmak için ctypes kütüphanesiyle devam ettim.
psapi = ctypes.WinDLL('psapi')
class PERFORMANCE_INFORMATION(ctypes.Structure):
    _DWORD = ctypes.c_ulong
    _SIZE_T = ctypes.c_size_t
    _fields_ = [
        ('cb', _DWORD),
        ('CommitTotal', _SIZE_T),
        ('CommitLimit', _SIZE_T),
        ('CommitPeak', _SIZE_T),
        ('PhysicalTotal', _SIZE_T),
        ('PhysicalAvailable', _SIZE_T),
        ('SystemCache', _SIZE_T),
        ('KernelTotal', _SIZE_T),
        ('KernelPaged', _SIZE_T),
        ('KernelNonpaged', _SIZE_T),
        ('PageSize', _SIZE_T),
        ('HandleCount', _DWORD),
        ('ProcessCount', _DWORD),
        ('ThreadCount', _DWORD),
    ]
    def __init__(self, getinfo=True, *args, **kwds):
        super(PERFORMANCE_INFORMATION, self).__init__(
              ctypes.sizeof(self), *args, **kwds)
        if (getinfo and not
            psapi.GetPerformanceInfo(ctypes.byref(self), 
                                     self.cb)):
            raise WinError()

    @property
    def cache_info(self):
        return self.SystemCache * self.PageSize
def get_cache_info():
    return PERFORMANCE_INFORMATION().cache_info


def get_disk_info():
    dict_={}

    for x in psutil.disk_partitions():
        if(x.fstype!=""):
            dict_[x.device]={"fstype":x.fstype,"disk_usege":psutil.disk_usage(x.device+"\\")}
    return dict_



# Create your views here.
def index(request):
        core=str(psutil.cpu_count())
        if request.method == 'POST':
            inputO = request.POST.get('message')
            calistir = subprocess.run(["powershell", "-Command", inputO], capture_output=True)
            success=calistir.stdout.decode('latin-1').splitlines()[7:]
            dnenem=""
            for x in success:
                dnenem+=x+" ;"
                
            if(success!=None):
                p = viewer_cmd(cmd_input=inputO,cmd_output=success)
                p.save()
            else:
                print("Error Null Variable")
            return HttpResponse(dnenem)



        disk_info=get_disk_info()
        cached=get_cache_info()
        all_data=viewer_cmd.objects.all().order_by('-id')[:10]

        content={'core':core,
        "cpu":psutil.cpu_times_percent(interval=1),
        "get_avg":psutil.getloadavg(),
        "cached":bytes2human(cached),
        "memory":psutil.virtual_memory(),
        "swap_mem":psutil.swap_memory(),
        "disks":disk_info,
        "physical_info":psutil.disk_io_counters("C:\\"),
        "show_tables":all_data,

        }
        time.sleep(0.4) # Broken pipe from ('127.0.0.1', 50296) Hatasından kaçınmak için.
        return render(request,"cek_app/index.html",content)


