
class Manual(object):

    def __init__(self, logger, hypervisors=None):
        self.logger = logger
        self.hypervisorList = hypervisors or []
        self._parse_hypervisor_list()

    def getHostGuestMapping(self):
        return self.hypervisors

    def ping(self):
        return True

    def _parse_hypervisor_list(self):
        self.hypervisors = dict([self._parse_hypervisor(line) for line in self.hypervisorList])

    def _parse_hypervisor(self, hypervisor_raw):
        '''
        takes a raw string such as "aaa-aaaa-aaa:bbb-ccc,ddd-eee" and parses it into
        a key, value tuple ("aaa-aaaa-aaa", ["bbb-ccc", "ddd-eee"])
        '''
        data_parts = hypervisor_raw.split(':')
        if len(data_parts) > 2 or not data_parts[0].strip():
            raise ValueError("Hypervisor info must take the form 'hypervisorId:guestid1,guestid2,etc'")

        hypervisor = data_parts[0].strip()
        guestIds = []
        if len(data_parts) == 2:
            guestIds = filter(None, [guest.strip() for guest in data_parts[1].split(',')])

        # Create full representation of the guest
        guests = [self._create_guest(guestId) for guestId in guestIds]
        return (hypervisor, guests)

    def _create_guest(self, guest_id):
        return {'guestId': guest_id,
                'attributes': {'virtWhoType': 'manual'}}
