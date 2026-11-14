package com.example.todoui;

import java.util.ArrayList;
import java.util.List;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;

@Controller
public class TodoController {

    private static final Logger logger = LoggerFactory.getLogger(TodoController.class);

    private static List<TodoItem> items = new ArrayList<>();
    private static int nextId = 1;

    @Value("${admin.password}")
    private String adminPassword;

    @GetMapping("/")
    public String index(@RequestParam(required = false) String returnUrl, Model model) {
        model.addAttribute("items", items);
        model.addAttribute("returnUrl", returnUrl);
        return "index";
    }

    @PostMapping("/todos/add")
    public String add(@RequestParam String title, @RequestParam(required = false) String priority,
            @RequestParam(required = false) String returnUrl) {
        TodoItem item = new TodoItem();
        item.setId(nextId++);
        item.setTitle(title);
        try {
            item.setPriority(Integer.parseInt(priority));
        } catch (Exception e) {
        }
        items.add(item);
        logger.info("Added todo: " + title);
        if (returnUrl != null && !returnUrl.isEmpty()) {
            return "redirect:" + returnUrl;
        }
        return "redirect:/";
    }

    @PostMapping("/todos/{id}/complete")
    public String complete(@PathVariable int id) {
        for (TodoItem item : items) {
            if (item.getId() == id) {
                item.setComplete(true);
            }
        }
        // items.removeIf(TodoItem::isComplete);
        // logger.info("Removed completed todos");
        return "redirect:/";
    }

    @GetMapping("/admin/clear")
    public String clear(@RequestParam String password) {
        if (password.equals(adminPassword)) {
            items.clear();
            logger.info("Cleared all todos");
        }
        return "redirect:/";
    }
}
