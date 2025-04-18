from finance_app.models import Category, Expense
from htpy import (
    Node,
    h2,
    html,
    img,
    script,
    table,
    td,
    th,
    head,
    meta,
    link,
    body,
    nav,
    div,
    button,
    span,
    a,
    li,
    title,
    tr,
    ul,
)
from flask import url_for


def int_to_money(cents: int):  # noqa: F811
    amt = cents / 100
    if amt < 0:
        return f"-${abs(amt):,.2f}"
    else:
        return f"${amt:,.2f}"


def nav_item_li(child: Node):
    return li(".nav-item")[child]


def base(content: Node, page_title: str = "Finance App"):
    return html()[
        head()[
            meta(charset="utf-8"),
            meta(
                name="viewport",
                content="width=device-width, initial-scale=1.0",
            ),
            title()[page_title],
            link(
                href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css",
                rel="stylesheet",
            ),
            link(
                rel="icon",
                href=url_for("static", filename="money.png"),
            ),
        ],
        body()[
            nav(".navbar.navbar-expand-lg")[
                div(".container-fluid")[
                    button(
                        ".navbar-toggler",
                        type="button",
                        data_bs_toggle="collapse",
                        data_bs_target="#navbarNav",
                        aria_controls="navbarNav",
                        aria_expanded="false",
                        aria_label="Toggle navigation",
                    )[
                        span(".navbar-toggler-icon"),
                    ],
                    div("#navbarNav.collapse navbar-collapse.justify-content-center")[
                        ul(".navbar-nav.hstack.gap-3")[
                            nav_item_li(
                                a(href=url_for("main.dashboard"))["Dashboard"],
                            ),
                            nav_item_li(
                                a(href=url_for("expenses.list_expenses"))["Expenses"]
                            ),
                            nav_item_li(
                                a(href=url_for("income.list_income"))["Income"]
                            ),
                        ]
                    ],
                ]
            ],
            div(".container")[content],
            script(
                src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js",
                integrity="sha384-C6RzsynM9kWDrMNeT87bh95OGNyZPhcTNXj1NW7RuBCsyN/o0jlpcV8Qyq46cDfL",
                crossorigin="anonymous",
            ),
        ],
    ]


def category_header(category: Category):
    return th(
        scope="row",
        style=f"background-color: #{category.color}",
    )[
        category.title,
    ]


def category_style(category: Category):
    balance = category.balance_current()
    if balance >= 0:
        return "background-color: #C6EFCE; color: #006100;"
    else:
        return "background-color: #FFC7CE; color: #9C0006;"


def monthly_balance(month_year, categories: list[Category], calendar):
    month = month_year[0]
    year = month_year[1]
    return tr()[
        td()[f"{calendar.month_name[month]} {year}"],
        [
            td(
                scope="row",
                style=f"background-color: #{category.color}",
            )[
                int_to_money(category.balance_for_month(year, month)),
            ]
            for category in categories
        ],
    ]


def dashboard(categories: list[Category], months, calendar) -> str:
    return str(
        base(
            [
                h2()["Category Balances:"],
                table(".table")[
                    [
                        tr()[
                            category_header(category),
                            td(scope="row", style=category_style(category))[
                                int_to_money(category.balance_current())
                            ],
                        ]
                        for category in categories
                    ]
                ],
                h2()["Monthly Balances"],
                table(".table")[
                    tr()[
                        th()["Month"],
                        [
                            th(style=f"background-color: #{category.color}")[
                                category.title
                            ]
                            for category in categories
                        ],
                    ],
                    [monthly_balance(month, categories, calendar) for month in months],
                ],
            ]
        )
    )


def list_expenses(expenses: list[Expense], next_url: str, prev_url: str):
    return str(
        base(
            [
                div(".d-flex.flex-row-reverse.mb-3")[
                    div(".btn-group")[
                        a(
                            ".btn.btn-secondary",
                            href=url_for("expenses.export_expenses"),
                        )[
                            "Export",
                        ],
                        a(
                            ".btn.btn-primary",
                            href=url_for("expenses.new_expense"),
                        )[
                            "New Expense",
                        ],
                    ]
                ],
                div(".table-responsive")[
                    table(".table")[
                        tr()[
                            th(scope="col")["Date"],
                            th(".text-center", scope="col")["Title"],
                            th(".text-center", scope="col")["Amount"],
                            th(".text-center", scope="col")["Category"],
                            th(".text-center", scope="col")["Tags"],
                            th(),
                        ],
                        [
                            tr()[
                                td()[expense.date.strftime("%m/%d/%y")],
                                td(".text-center")[
                                    a(href=url_for("expenses.expense", id=expense.id))[
                                        expense.title,
                                    ],
                                ],
                                td(".text-center")[expense.formatted_amount()],
                                td(
                                    ".text-center",
                                    style=f"background: #{expense.category.color}",
                                )[
                                    expense.category.title,
                                ],
                                td(".text-center")[
                                    [
                                        span(
                                            ".badge",
                                            style=f"background-color: #{expense_tag.tag.color}",
                                        )[
                                            expense_tag.tag.name,
                                        ]
                                        for expense_tag in expense.tags
                                    ]
                                ],
                                td()[
                                    a(
                                        href=url_for(
                                            "expenses.delete_expense",
                                            id=expense.id,
                                        )
                                    )[
                                        img(
                                            src=url_for(
                                                "static",
                                                filename="delete.svg",
                                                alt="Delete",
                                            )
                                        )
                                    ]
                                ],
                            ]
                            for expense in expenses
                        ],
                    ]
                ],
                div(".d-flex.justify-content-between.mb-3")[
                    div()[a(href=prev_url)["< Previous Page"] if prev_url else None],
                    div()[a(href=next_url)["Next Page >"] if next_url else None],
                ],
            ]
        )
    )
