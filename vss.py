import win32com.client

class ShadowCopy(object):
    def __init__(self, drives):
        self._drives = set()
        self._shadow_guids = {}
        self._shadow_paths = {}
        for d in drives:
            self._add_drive(d)

    def close(self):
        for guid in self._shadow_guids.values():
            self._vss_delete(guid)
    
    def shadow(self, drive):
        return self._shadow_paths[drive]

    # Leaky abstraction, maybe just wrap a single volume.
    def __enter__(self):
        return self._shadow_paths
    
    def __exit__(self, type, value, traceback):
        self.close()

    def _add_drive(self, drive):
        if drive not in self._drives:
            self._drives.add(drive)
            self._shadow_guids[drive] = self._vss_create(drive)
            self._shadow_paths[drive] = \
                self._vss_path(self._shadow_guids[drive])

    def _vss_path(self, guid):
        wcd = win32com.client.Dispatch('WbemScripting.SWbemLocator')
        wmi = wcd.ConnectServer('.', 'root\\cimv2')
        obj = wmi.ExecQuery(
            f'SELECT * FROM Win32_ShadowCopy WHERE ID="{guid}"')
        return obj[0].DeviceObject
    
    def _vss_create(self, drive):
        sc = win32com.client.GetObject(
            'winmgmts:\\\\.\\root\\cimv2:Win32_ShadowCopy'
        )
        params = sc.Methods_('Create').InParameters
        params.Properties_[1].value = f'{drive}:\\'
        results = sc.ExecMethod_('Create', params)
        # First is return code, second is GUID.
        return results.Properties_[1].value
    
    def _vss_delete(self, guid):
        wcd = win32com.client.Dispatch('WbemScripting.SWbemLocator')
        wmi = wcd.ConnectServer('.', 'root\\cimv2')
        obj = wmi.ExecQuery(
            f'SELECT * FROM Win32_ShadowCopy WHERE ID="{guid}"')
        obj[0].Delete_()

