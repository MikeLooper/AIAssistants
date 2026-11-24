package com.example.todoapi;

import java.util.List;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class CustomerController {

    @GetMapping("/customers")
    public List<Customer> list() {
        return CustomerSeed.CUSTOMERS;
    }

    @GetMapping("/customers/lookup")
    public ResponseEntity<Customer> lookup(@RequestParam String email) {
        return CustomerSeed.CUSTOMERS.stream()
                .filter(c -> c.email().equals(email))
                .findFirst()
                .map(ResponseEntity::ok)
                .orElse(ResponseEntity.notFound().build());
    }
}
