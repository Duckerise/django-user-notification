class NotificationException(Exception):
    pass


class InvalidEventIdentifierFormat(NotificationException):
    pass


class RelatedUserNotFound(NotificationException):
    pass


class RelatedEventNotFound(NotificationException):
    pass


class RelatedSenderClassNotFound(NotificationException):
    pass


class MultipleNotificationsFound(NotificationException):
    pass


class NotificationAlreadySent(NotificationException):
    pass


class NotificationFollowUpEventException(NotificationException):
    pass


class NotificationDisabled(NotificationException):
    pass
