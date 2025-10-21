import atexit
from functools import wraps

from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask


class FlaskScheduler(BackgroundScheduler):
    app: Flask

    def init_app(self, app: Flask):
        self.app = app
        self.start()
        atexit.register(lambda: self.shutdown())

    def add_job(
        self,
        func,
        trigger=None,
        args=None,
        kwargs=None,
        id=None,
        name=None,
        misfire_grace_time=...,
        coalesce=...,
        max_instances=...,
        next_run_time=...,
        jobstore="default",
        executor="default",
        replace_existing=False,
        **trigger_args,
    ):
        # Create a wrapper around the job function that pushes the
        # Flask app context before calling the job function, so
        # that we can rely on the app context existing within the job
        # function, for functionality such as SQLAlchemy DB calls.
        # Use the @wraps decorator so that the wrapper function uses
        # the correct name of the wrapped function.
        @wraps(func)
        def wrap_func(*args, **kwargs):
            with self.app.app_context():
                func(*args, **kwargs)

        return super().add_job(
            # Add the wrapper function to the job
            # instead of the original function
            wrap_func,
            trigger,
            args,
            kwargs,
            id,
            name,
            None,  # misfire_grace_time
            coalesce,
            max_instances,
            next_run_time,
            jobstore,
            executor,
            replace_existing,
            **trigger_args,
        )
