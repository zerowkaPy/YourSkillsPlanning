
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types.user import User



class SmartKeyboard:
    _instance = {}  # {user_id : instance}

    def __new__(cls, from_user: User):
        user_id = str(from_user.id)
        if user_id in cls._instance:
            return cls._instance[user_id]
        instance = super().__new__(cls)
        cls._instance[user_id] = instance
        return instance

    def __init__(self, user_id):
        if hasattr(self, "_initialized"):
            return
        self._user_id = str(user_id)
        self._initialized = True  # флаг ініціалізації екземпляру
        self._kb_init = False #флаг ініціалізації клавіатури

    def init_keyboard(self):
        self._adjust = None
        self._buttons = None
        self._page_num = None
        self._rest = None
        self._rows_num = None
        self._next_button = None
        self._back_button = None
        self._home_button = None
        self._pages = {}
        self._pages_prop = {}
        self._count = 1

        self._kb_init = True

    @classmethod
    def delete_user(cls, from_user:User):
        user_id = str(from_user.id)
        cls._instance.pop(user_id)

    def _kb_prop(self):
        self._page_num = len(self._buttons) // self._rows_num
        self._rest = len(self._buttons) % self._rows_num

        if self._rest:
            self._page_num = self._page_num+1

    def _prop_check(self):
        if self._adjust:
            return True
        else:
            return False

    def set_prop(self, adjust:list[int], rows_num:int, next_button:str = "next", back_button:str = "back", home_button :str = None):
        if not self._buttons:
            raise SyntaxError("you must first execute 'add_buttons'")
        self._adjust = adjust
        self._rows_num = rows_num
        self._next_button = next_button
        self._back_button = back_button
        self._home_button = home_button
        self._kb_prop()

        for page in range(self._page_num):
            page +=1
            self._pages[str(page)] = [button for button in self._buttons[:self._rows_num]]
            self._buttons = self._buttons[self._rows_num:]
            self._last_page = page

        if self._rest:
            self._pages[str(self._last_page+1)] = [button for button in self._buttons]
            self._buttons.clear()

        for page in range(self._page_num):
            page+=1
            if self._page_num == 1 and self._rest == 0:
                self._pages_prop[str(page)] = "none"
            elif page == 1:
                self._pages_prop[str(page)] = "n"
            elif self._page_num - page == 0 and self._rest:
                self._pages_prop[str(page)] = 'b'
            elif self._page_num - page == 0:
                self._pages_prop[str(page)] = "b"
            else:
                self._pages_prop[str(page)] = "bn"


    def add_butons(self, buttons:list[str]):
        if not self._kb_init:
            raise RuntimeError("you must execute init_keyboard before call add_butons")
        if type(buttons) != list:
            raise TypeError("buttons parameter must be a list of strings")
        if len(buttons) == 0:
            raise ValueError("buttons parameter must contain at least 1 string")
        self._buttons = buttons

        self._kb_init = False

        
    def get_keyboard(self):
        if self._prop_check():
            builder = InlineKeyboardBuilder()
            page = self._pages_prop[str(self._count)]
            if page == 'none':
                for button in self._pages[str(self._count)]:
                    builder.add(InlineKeyboardButton(text=button, callback_data=button))
                builder.adjust(*self._adjust)
                adjust = [*self._adjust]
                self._count +=1
            elif page == 'n':
                for button in self._pages[str(self._count)]:
                    builder.add(InlineKeyboardButton(text=button, callback_data=button))
                builder.add(InlineKeyboardButton(text=self._next_button, callback_data=self._next_button))
                builder.adjust(*self._adjust, 1)
                adjust = [*self._adjust, 1]
                self._count +=1
            elif page == 'bn':
                for button in self._pages[str(self._count)]:
                    builder.add(InlineKeyboardButton(text=button, callback_data=button))
                builder.add(InlineKeyboardButton(text=self._back_button, callback_data=self._back_button))
                builder.add(InlineKeyboardButton(text=self._next_button, callback_data=self._next_button))
                builder.adjust(*self._adjust, 2)
                adjust = [*self._adjust, 2]
                self._count +=1
            elif page == 'b':
                for button in self._pages[str(self._count)]:
                    builder.add(InlineKeyboardButton(text=button, callback_data=button))
                builder.add(InlineKeyboardButton(text=self._back_button, callback_data=self._back_button))
                builder.adjust(*self._adjust, 1)
                adjust = [*self._adjust, 1]
                self._count +=1

            if self._home_button:
                builder.add(InlineKeyboardButton(text=self._home_button, callback_data=self._home_button))
                builder.adjust(*adjust, 1)
            return builder.as_markup()
        else:
            raise RuntimeError("You must execute set_prop() before calling get_keyboard()")
        
    def previous_keyboard(self):
        builder = InlineKeyboardBuilder()
        count = self._count - 2
        self._count -=1
        page = self._pages_prop[str(count)]
        if page == 'n':
            for button in self._pages[str(count)]:
                builder.add(InlineKeyboardButton(text=button, callback_data=button))
            builder.add(InlineKeyboardButton(text=self._next_button, callback_data=self._next_button))
            builder.adjust(*self._adjust, 1)
            adjust = [*self._adjust, 1]
        elif page == 'bn':
            for button in self._pages[str(count)]:
                builder.add(InlineKeyboardButton(text=button, callback_data=button))
            builder.add(InlineKeyboardButton(text=self._back_button, callback_data=self._back_button))
            builder.add(InlineKeyboardButton(text=self._next_button, callback_data=self._next_button))
            builder.adjust(*self._adjust, 2)
            adjust = [*self._adjust, 2]

        if self._home_button:
                builder.add(InlineKeyboardButton(text=self._home_button, callback_data=self._home_button))
                builder.adjust(*adjust, 1)
        return builder.as_markup()
