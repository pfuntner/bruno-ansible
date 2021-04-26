function j2_script {
  echo 'lines: {{ lines | length }}'
}

echo "lines:
  - line 1
  - line 2" | j2 --format=yaml <(j2_script)

echo '{"lines": ["line 1", "line 2" ]}' | j2 --format=json <(j2_script)
