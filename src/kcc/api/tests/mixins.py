from unittest.mock import patch


class ContactMomentSyncMixin:
    def setUp(self):
        super().setUp()

        patcher_sync_create = patch("kcc.sync.signals.sync_create_contactmoment")
        self.mocked_sync_create = patcher_sync_create.start()
        self.addCleanup(patcher_sync_create.stop)

        patcher_sync_delete = patch("kcc.sync.signals.sync_delete_contactmoment")
        self.mocked_sync_delete = patcher_sync_delete.start()
        self.addCleanup(patcher_sync_delete.stop)
