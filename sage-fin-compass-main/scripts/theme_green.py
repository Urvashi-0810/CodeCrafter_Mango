import sys
import re

file_path = 'c:/Users/urvas/OneDrive/Desktop/CodeCrafters/CodeCrafter_Mango/sage-fin-compass-main/src/pages/Portfolio.tsx'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

replacements = [
    # Explicit hex codes used for the blue theme
    (r'text-\[\#0f62fe\]', 'text-primary'),
    (r'bg-\[\#0f62fe\]', 'bg-primary'),
    (r'border-\[\#0f62fe\]', 'border-primary'),
    (r'bg-\[\#e0eafe\]', 'bg-primary/20'),
    (r'bg-\[\#f8faff\]', 'bg-primary/5'),
    (r'hover:bg-\[\#0353e9\]', 'hover:bg-primary/90'),
    
    # Tailwind blue classes
    (r'bg-blue-50(?!/)', 'bg-primary/10'),
    (r'bg-blue-50/70', 'bg-primary/10'),
    (r'bg-blue-600', 'bg-primary'),
    (r'border-blue-100', 'border-primary/20'),
    
    (r'text-blue-400', 'text-primary'),
    (r'text-blue-500', 'text-primary'),
    (r'text-blue-600', 'text-primary'),
    (r'text-blue-700', 'text-primary-foreground'),
    
    (r'hover:bg-blue-100', 'hover:bg-primary/20'),
    (r'hover:text-blue-700', 'hover:text-primary-foreground'),
    
    # Dark mode blues
    (r'dark:bg-blue-900/10', 'dark:bg-primary/10'),
    (r'dark:bg-blue-900/20', 'dark:bg-primary/20'),
    (r'dark:bg-blue-900/30', 'dark:bg-primary/30'),
    (r'dark:bg-blue-900/40', 'dark:bg-primary/40'),
    (r'dark:bg-blue-900/50', 'dark:bg-primary/50'),
    
    (r'dark:border-blue-400', 'dark:border-primary/50'),
    (r'dark:border-blue-900/30', 'dark:border-primary/30'),
    (r'dark:border-blue-900/40', 'dark:border-primary/40'),
    
    (r'dark:text-blue-400', 'dark:text-primary'),
    (r'dark:text-blue-500', 'dark:text-primary/80'),
]

for old, new in replacements:
    content = re.sub(old, new, content)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Portfolio theme replaced successfully!")
