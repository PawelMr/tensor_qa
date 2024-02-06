from atf.ui import *
from pages.saby_pages.AuthOnline import AuthOnline
from pages.saby_pages.Plans import Plans
from atf import *
import datetime
from atf.api.json_rpc import JsonRpcClient
from api.wrappers.work_plan_api_wrappers import WorkPlanApiWrappers
from api.clients.document_api import DocumentApi


class TestPlane(TestCaseUI):
    """Проверка страницы планы"""
    client_api = None

    @classmethod
    def setUpClass(cls):
        """для всего класса тестов авторизация и создание экземпляра класса проверки планов"""
        AuthOnline(cls.driver).auth(cls.config.get('USER_LOGIN'), cls.config.get('USER_PASSWORD'),
                                    cls.config.get('SITE'))
        cls.page_planes = Plans(cls.driver)
        cls.client_api = JsonRpcClient(url=cls.config.get('SITE'), verbose_log=0)
        cls.client_api.auth(login=cls.config.get("USER_LOGIN"), password=cls.config.get("USER_PASSWORD"))
        cls.work_plan_api = WorkPlanApiWrappers(cls.client_api)
        cls.doc_api = DocumentApi(cls.client_api)

    def setUp(self):
        """для каждого теста проверка прогрузки списка планов"""
        self.page_planes.open_page()
        self.page_planes.check_load_plans()

    def tearDownClass(cls):
        """
        удаляем планы с комментарием "plan_autotest"
        """
        log("удаляем через апи")
        list_id = cls.work_plan_api.get_list_id_plans(mask_comment="plan_autotest")
        for i in list_id:
            cls.doc_api.delete_doc(i)

    def test_01(self):
        """
        Создайте план работ
        Выберите объект планирования через панель выбора.
        Укажите заказчика
        Добавьте пункт плана, указав описание и исполнителя
        Запустите план в документооборот
        Откройте созданный план и убедитесь, что пункт плана, заказчик и исполнитель отображаются согласно
        введенным ранее данным
        Удалите созданный план через реестр
        Убедитесь, что план не отображается в реестре.
        """
        log("Создаем план")
        self.page_planes.create_document('План работ')
        from pages.PM.Plans.dialog import Dialog as DialogPlans
        plan = DialogPlans(self.driver)
        plan.check_open()

        log("Выбираем исполнителя")
        plan.select_executor("Крошелев")

        # не по заданию но что бы схему легче было почистить потом
        log("указываем коментарий к плану")
        comment = f'plan_autotest {datetime.datetime.now()}'
        plan.enter_comment(comment)

        log("выбираем заказчика(ответственного)")
        plan.choose_employer("Крошелев")

        log("добавляем пункт плана")
        plan.add_element_in_empty_plan("Пункт плана")
        from pages.PM.Plans.point import Dialog as DialogPoint
        point = DialogPoint(self.driver)
        point.check_open()

        log("указываем описание пункта плана")
        comment2 = f'point_autotest {datetime.datetime.now()}'
        point.enter_comment(comment2)

        log("выбираем исполнителя пункта плана")
        point.add_executor.click()
        from pages.Staff.selection import Stack as ListStaff
        staff = ListStaff(self.driver)
        staff.select("Крошелев")
        staff.check_close()

        log("сохраняем пункт плана")
        point.save_point()
        point.check_close()

        log("запускаем план на выполнение закрываем")
        plan.launch_plan()

        log("открываем план проверяем объект планирования, заказчика, наличие пункта с заданным коментарием")
        self.page_planes.open_plans(comment2)
        plan.check_open()
        plan.check_executor("Крошелев Александр Алексеевич")
        plan.check_employer("Крошелев А.А.")
        plan.check_point(comment2)

        log("закрываем план")
        plan.close()
        plan.check_close()

        log("удаляем через апи")
        list_id = self.work_plan_api.get_list_id_plans(item_comment=comment2)
        for i in list_id:
            self.doc_api.delete_doc(i)
        self.page_planes.open_page()
        self.page_planes.check_load_plans()

        log("проверяем что в списке с комментарием пункта план не отображается")
        self.page_planes.check_list_plans(comment2, False)
