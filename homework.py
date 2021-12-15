from dataclasses import dataclass, fields
from typing import ClassVar


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    PYTKA_POPYTKA: ClassVar[str] = (
        'Тип тренировки: {}; '
        'Длительность: {:.3f} ч.; '
        'Дистанция: {:.3f} км; '
        'Ср. скорость: {:.3f} км/ч; '
        'Потрачено ккал: {:.3f}.'
    )

    def get_message(self) -> str:
        return self.PYTKA_POPYTKA.format(
            self.training_type, self.duration,
            self.distance, self.speed,
            self.calories
        )


@dataclass
class Training:
    """Базовый класс тренировки."""
    LEN_STEP: ClassVar[float] = 0.65
    M_IN_KM: ClassVar[int] = 1000
    H_IN_M: ClassVar[int] = 60

    action: int
    duration: float
    weight: float

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            self.__class__.__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories()
        )


class Running(Training):
    """Тренировка: бег."""
    MUR_MUR_1: ClassVar[float] = 18
    MUR_MUR_2: ClassVar[float] = 20

    def get_spent_calories(self) -> float:
        return (((self.MUR_MUR_1 * self.get_mean_speed())
                - self.MUR_MUR_2) * self.weight / self.M_IN_KM
                * self.duration * self.H_IN_M)


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    PUP_PUP_1: ClassVar[float] = 0.035
    PUP_PUP_2: ClassVar[float] = 0.029
    height: float

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return (((self.PUP_PUP_1 * self.weight)
                + ((self.get_mean_speed()**2 // self.height)
                * self.PUP_PUP_2 * self.weight))
                * self.duration * self.H_IN_M)


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""
    WOB_WOB_1: ClassVar[float] = 1.1
    WOB_WOB_2: ClassVar[float] = 2
    LEN_STEP: ClassVar[float] = 1.38
    length_pool: float
    count_pool: int

    def get_mean_speed(self) -> float:
        """Средняя скорость."""
        return (
            self.length_pool * self.count_pool
            / self.M_IN_KM / self.duration
        )

    def get_spent_calories(self) -> float:
        """Спаленные калории"""
        return (
            (self.get_mean_speed() + self.WOB_WOB_1)
            * self.WOB_WOB_2 * self.weight
        )


TRAINING_TYPE = {'SWM': Swimming, 'RUN': Running, 'WLK': SportsWalking}
TRAINING_ERROR_404 = 'Упс, нет такой тренировки {}'


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    if workout_type in TRAINING_TYPE:
        tested_class = TRAINING_TYPE.get(workout_type)
        error_info(tested_class, data)
        return TRAINING_TYPE.get(workout_type)(*data)
    raise ValueError(TRAINING_ERROR_404.format(workout_type))


def main(training: Training) -> None:
    """Главная функция."""
    print(training.show_training_info().get_message())


def error_info(tested_class, data):
    number_of_class_fields = len(fields(tested_class))
    if number_of_class_fields != len(data):
        raise TypeError('Ожиалось другое число аргументов')


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180])
    ]

    for workout_type, data in packages:
        main(read_package(workout_type, data))
