function! StartSourceKittenDaemon(project_name, port, ... )
  let l:job = "sourcekittendaemon start --project " . a:project_name " --port " . a:port
  let g:source_kitten_job_id = jobstart(l:job)
endfunction

function! StopSourceKittenDaemon()
  call jobstop(g:source_kitten_job_id)
endfunction
