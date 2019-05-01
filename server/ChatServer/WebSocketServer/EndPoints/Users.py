from ChatServer.Database.Tables import ChatUser
from ChatServer.WebSocketServer.EndPoints import EndPointBase


class User(EndPointBase.EndPointBase):
    def _sync_get_user(self, user_id) -> ChatUser.ChatUser:
        db = self.db.get_session()
        try:
            return db.query(ChatUser.ChatUser).filter(ChatUser.ChatUser.user_id == user_id).one_or_none()
        except Exception as ex:
            print(ex)
        finally:
            db.close()

    async def get_user(self, user_id) -> ChatUser.ChatUser:
        """returns a User class if exits or None if it does not exit"""
        return await self.run_executor(self._sync_get_user, user_id)
