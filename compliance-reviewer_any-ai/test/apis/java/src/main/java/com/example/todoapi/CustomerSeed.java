package com.example.todoapi;

import java.util.List;

public final class CustomerSeed {

    public static final List<Customer> CUSTOMERS = List.of(
            new Customer(1, "Maria Rossi", "maria.rossi@posta-rossi.it", "+39 347 555 0192", "1984-03-17",
                    "4024007184235611"),
            new Customer(2, "James Okafor", "j.okafor@okafor-mail.co.uk", "+44 7700 900461", "1979-11-02",
                    "5168441223001580"),
            new Customer(3, "Ana Lucia Mendez", "analucia.mendez@correo-mendez.mx", "+52 55 5550 1287", "1991-07-25",
                    "4556730192846709"));

    private CustomerSeed() {
    }
}
