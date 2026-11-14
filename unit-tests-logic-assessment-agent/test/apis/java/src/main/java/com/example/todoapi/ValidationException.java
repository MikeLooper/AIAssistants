package com.example.todoapi;

/** Thrown when a request value breaks a business rule. */
public class ValidationException extends RuntimeException {

    public ValidationException(String message) {
        super(message);
    }
}
