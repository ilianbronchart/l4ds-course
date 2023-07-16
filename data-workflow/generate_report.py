import os
import shutil
from jinja2 import Environment, FileSystemLoader
# from github import Github

# Set up Jinja2 template environment
env = Environment(loader=FileSystemLoader('.'))
template = env.get_template('report_template.html')

# Get list of report files
reports_dir = './reports'
report_dirs = [d for d in os.listdir(reports_dir) if os.path.isdir(os.path.join(reports_dir, d))]
latest_report = sorted(report_dirs)[-1]

# Render HTML template with image file paths and timestamp
timestamp = os.path.basename(latest_report).split('-')[1].replace(':', '-')
html = template.render(timestamp=timestamp)

if not os.path.exists('./docs'):
    os.makedirs('./docs')

# Copy all files from latest_report directory to docs directory
for file_name in os.listdir(f'./reports/{latest_report}'):
    shutil.copy(f'./reports/{latest_report}/{file_name}', f'./docs/{file_name}')

# Save report.html to docs directory
with open(f'./docs/index.html', 'w') as f:
    f.write(html)

